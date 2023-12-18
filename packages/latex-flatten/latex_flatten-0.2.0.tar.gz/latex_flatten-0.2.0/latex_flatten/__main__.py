# system modules
import argparse
import os
import sys
import glob
import re
import itertools
from pathlib import Path
import shutil
import tempfile
import logging
from pathlib import Path
from zipfile import ZipFile
import inspect

# external modules
import rich
import rich.box
from rich.syntax import Syntax
from rich.panel import Panel
from rich.table import Table
from rich.pretty import Pretty
from rich.logging import RichHandler
from rich.console import Console

console = Console()

logger = logging.getLogger(__name__)


def two_at_a_time(iterable):
    """
    Yields two elements of an iterable at a time. Non-full two-pairs are
    ignored, e.g. when ``iterable`` as an odd numbero of elements.
    """
    iterable = iter(iterable)
    while True:
        try:
            yield next(iterable), next(iterable)
        except StopIteration:
            break


def batch_replace(x, replacements, offset=0):
    """
    Replace regions in a bytestring all at once. Mapping is like ``{(10,23):b"blubb",...}``.
    The ``offset`` will be subtracted from the positions. Useful to
    batch-replace regex ``match.span`` regions.
    """
    parts = []
    for (left, right), replacement in itertools.zip_longest(
        two_at_a_time(
            itertools.chain([0], itertools.chain.from_iterable(replacements), [None])
        ),
        replacements.values(),
        fillvalue=b"",
    ):
        left -= offset
        if right is not None:
            right -= offset
        parts.append(x[left:right])
        parts.append(replacement)

    result = b"".join(parts)

    for replacement in replacements.values():
        if replacement not in result:
            logger.error(
                rf"{replacement[:30] = } did not work in {x[:50]!r}. This should not happen."
            )

    return result


def formatstr(x):
    try:
        x.format(1)
    except Exception as e:
        raise argparse.ArgumentTypeError(
            f"{x!r} can not be format()ed with a single argument: {e!r}"
        )
    return x.format


def present_latex(code, changed=None, title=None):
    if hasattr(code, "decode"):
        code = code.decode(errors="ignore")
    if hasattr(changed, "decode"):
        changed = changed.decode(errors="ignore")
    if changed is None:
        output = Syntax(code, lexer="latex")
        if title:
            output = Panel(output, title=title)
        console.log(output)
    else:
        table = Table(
            title=title,
            box=rich.box.ROUNDED,
            padding=0,
            expand=True,
        )
        table.add_column("before", ratio=1, justify="center", no_wrap=True)
        table.add_column("after", ratio=1, justify="center", no_wrap=True)
        if len(lines := changed.splitlines()) > (
            nlines := int(os.environ.get("LATEX_FLATTEN_DIFF_LENGTH", 10))
        ):
            changed = os.linesep.join(lines[:nlines] + ["…"])
        table.add_row(
            Syntax(
                code,
                lexer="latex",
                word_wrap=False,
            ),
            Syntax(
                changed,
                lexer="latex",
                word_wrap=False,
            ),
        )
        console.log(table)


def process(
    texcode=None,
    texfile=None,
    texfiledir=None,
    writeout=False,
    args=argparse.Namespace(),
):
    r"""
    Recursively replace every \input{FILE} in a given ``texfile`` or
    ``texcode`` with the contents of FILE. If the ``texfile`` has been
    moved for editing, ``texfiledir`` can be set to the working directory
    for reference of the inclusion paths. ``writeout`` causes the
    updated version to be written to ``texfile``.

    Yields:
        Path: path that should not be included in the outdir or ZIP as it has been replaced
        bytes: the updated TeX code
    """
    frame = inspect.currentframe()
    recursion_level = (
        len([f for f in inspect.getouterframes(frame) if f.function == "process"]) - 1
    )
    if logger.getEffectiveLevel() < logging.DEBUG:
        logger.debug(
            f"process({(texcode or b'')[:50] = }, {texfile = }, {texfiledir = }, {writeout = }), {recursion_level = }"
        )
    if texfile is None:
        texfiledir = Path(".")
    if texfiledir is None:
        texfiledir = texfile.parent
    texfiledir = texfiledir or Path(texfiledir)
    texfile = texfile or Path(texfile)
    if texcode is None:
        if texfile is None:
            logger.error(f"process(): Neither texfile nor texcode given.")
            return
        try:
            with texfile.open("rb") as fh:
                texcode = fh.read()
        except Exception as e:
            logger.error(f"process(): Couldn't read {texfile = !r}: {e!r}.")
            return

    logger.debug(
        f"process({texcode[:50] = }, {texfile = }, {texfiledir = }, {writeout = })"
    )

    if logger.getEffectiveLevel() <= logging.INFO - 10 * recursion_level and texfile:
        console.log(Panel(f"Processing [code]{str(texfile)!r}[/code]"))

    logger.info(
        rf"{str(texfile)!r}: Searching occurences of \input{{FILE}} to replace with contents of FILE"
    )
    texcode_replacements = dict()
    for n, match in enumerate(
        re.finditer(
            rb"^(?P<fullline>(?P<prefix>.*?)(?P<inputcmd>\\input\s*\{\s*(?P<inputfile>[^}]+)\s*\})(?P<suffix>.*))$",
            texcode,
            flags=re.MULTILINE,
        )
    ):
        fullline = match.groupdict()["fullline"]
        inputcmd = match.groupdict()["inputcmd"]
        inputfile = match.groupdict()["inputfile"].strip()
        if re.search(rb"(?![\\])%", match.groupdict()["prefix"]):
            logger.debug(rf"🙈 Ignoring commented {inputcmd!r}")
            continue
        logger.info(rf"{str(texfile)!r}: Found \input line #{n}")
        if logger.getEffectiveLevel() < logging.INFO - 10 * recursion_level:
            present_latex(fullline)
        inputfilepath = Path(inputfile.decode(errors="ignore"))
        inputfile = inputfilepath
        # 🔄 !!!RECURSION!!!
        inputfilecontent = None
        for result in process(
            texfile=inputfile if inputfile.is_absolute() else texfiledir / inputfile,
            texfiledir=texfiledir if inputfile.is_absolute() else texfiledir,
            args=args,
        ):
            if isinstance(result, bytes):
                if inputfilecontent is None:
                    inputfilecontent = result
                else:
                    logger.error(
                        f"🐛 BUG: There is already an inputfilecontent for {str(inputfile)!r} {inputfilecontent[:50]!r}. "
                        f"Ignoring new one {result[:50]!r}."
                    )
                continue
            yield result
        if inputfilecontent is None:
            logger.error(
                rf"No content for \input file {str(inputfile)!r} came back. Skipping."
            )
            continue
        logger.debug(
            f"{len(inputfilecontent)} bytes ({len(inputfilecontent.splitlines())} lines) came back for processed {str(inputfile)!r}"
        )
        logger.info(
            f"{str(texfile)!r}: ✂️  Replacing {inputcmd!r} with contents of {str(inputfile)!r} ({len(inputfilecontent.splitlines())} lines)"
        )
        # replace the original full matched line region with the updated content
        texcode_replacements[match.span("inputcmd")] = inputfilecontent

        # replace the \input in the full line match (so we can show a diff below, just nice to have)
        fullline_updated = batch_replace(
            fullline,
            offset=match.span("fullline")[0],  # we operate within the 'fullline' match
            replacements={match.span("inputcmd"): inputfilecontent},
        )
        if logger.getEffectiveLevel() <= logging.INFO - 10 * recursion_level:
            present_latex(
                fullline,
                fullline_updated,
                title=f"[bold]{texfile}[/bold]:\nReplacing [code]\input{{{inputfile}}}[/code] with the file contents",
            )

        yield inputfilepath  # Path yielded: This dependent file is not needed anymore

    texcode = batch_replace(texcode, texcode_replacements)

    if texfile and writeout:
        with open(texfile, "wb") as fh:
            fh.write(texcode)
            logger.info(f"💾 Saved {str(texfile)!r}")

    yield texcode


parser = argparse.ArgumentParser(
    description="Turn your latex LaTeX project into a flat structure or ZIP file"
)
parser.add_argument(
    "texfiles",
    nargs="*",
    default=(_ := glob.glob("*.tex")),
    help="TeX files to process. " f"Defaults to {', '.join(map(repr,_))}.",
)

behaviourgroup = parser.add_argument_group(
    title="Processing", description="Options changing the processing behaviour"
)
behaviourgroup.add_argument(
    "--plos",
    help="activate PLoS settings (shorthand for --replace-bib --sequential-figures --hide-figures)",
    action="store_true",
)
behaviourgroup.add_argument(
    "--replace-bib",
    help=r"replace \bibliography with .bbl contents (needed for PLoS)",
    action="store_true",
)
behaviourgroup.add_argument(
    "--sequential-figures",
    metavar="FORMATSTR",
    const=(
        default_sequential_figures := (
            default_sequential_figures_format := "fig{}"
        ).format
    ),
    type=formatstr,
    help=f"[RUDIMENTARY] Rename figure files sequentially (default e.g. {default_sequential_figures(3)+'.ext'!r}). "
    "Can be set to a Python format string where {} is replaced with the figure number. "
    f"Default format is {default_sequential_figures_format!r}. "
    f"Note that the resulting figure numbers might not correspond to the actual figure labels.",
    nargs="?",
)
behaviourgroup.add_argument(
    "--hide-figures",
    help="[RUDIMENTARY] Hide graphics (by not \includegraphics{}ing them). "
    f"The source files are still included. "
    f"Note that also graphics that are not actually figures might be hidden. ",
    action="store_true",
)


outputgroup = parser.add_argument_group(
    title="Output", description="Options changing the output behaviour"
)
outputgroup.add_argument(
    "--inplace",
    help=r"modify TeX files in-place and place source files around it.",
    action="store_true",
)
outputgroup.add_argument(
    "-d",
    "--outdir",
    help=r"output directory for files (if --inplace is not given). "
    "By default, a temporary directory is used that is later removed.",
)
outputgroup.add_argument(
    "-z",
    "--zip",
    help=r"Make a ZIP file next to the .tex file with the adjusted .tex file "
    "and its dependencies in a flat structure as in --outdir. ",
    action="store_true",
)
outputgroup.add_argument(
    "--keep-other-files",
    help="Also include .aux etc. files",
    action="store_true",
)
outputgroup.add_argument(
    "--copy",
    help="Copy files instead of symlinking.",
    action="store_true",
)
outputgroup.add_argument(
    "--force",
    help="Just do it. Potentially overwrites files and loses data.",
    action="store_true",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)


def cli():
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO - (args.verbose - args.quiet) * 5,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )

    if args.plos:
        args.replace_bib = True
        args.sequential_figures = default_sequential_figures
        args.hide_figures = True

    if args.sequential_figures:
        logger.warning(
            f"--sequential-figures is implemented rudimentally and might not reflect the actual figure number correctly."
        )

    if args.hide_figures:
        logger.warning(
            f"--hide-figures is implemented rudimentally and might also hide graphics that are not actually figures."
        )

    # make the most out of given command-line arguments
    expanded_texfiles = []
    for texfile in args.texfiles:
        path = Path(texfile)
        if path.is_dir():
            if texfiles_here := list(map(str, path.glob("*.tex"))):
                expanded_texfiles.extend(texfiles_here)
                logger.info(
                    f"Found {len(texfiles_here)} .tex files {texfiles_here} in given directory {texfile!r}, using those instead."
                )
            else:
                logger.warning(
                    f"No .tex files in given directory {texfile!r}. Skipping."
                )
        elif path.is_file():
            expanded_texfiles.append(texfile)
        else:
            logger.warning(
                f"Given path {texfile!r} is neither an existing file nor a directory containing .tex files. Skipping."
            )
    args.texfiles = expanded_texfiles
    if not args.texfiles:
        logger.info(f"😴 No TeX files. Nothing to do.")
        sys.exit(0)

    if not (args.inplace or args.outdir or args.zip):
        logger.warning(
            f"If neither --inplace, --outdir or --zip is given, you won't see much of an effect. Continuing anyway."
        )

    if len(args.texfiles) > 1 and args.outdir:
        logger.critical(
            f"Giving an --outdir while specifying {len(args.texfiles)} .tex files {tuple(args.texfiles)} is not sensible. "
            "Use --force to do it anyway."
        )
        sys.exit(2)

    logger.debug(f"{args = }")

    logger.info(
        f"{len(args.texfiles)} TeX files to process. {', '.join(map(repr,args.texfiles))}"
    )

    def readInputFiles(texfile):
        texfile = Path(texfile)
        pattern = re.compile(r"^INPUT\s+(?P<file>.*)$")
        if (flsfile := texfile.parent / Path(f"{texfile.stem}.fls")).exists():
            logger.debug(f"{str(texfile)!r}: Found {str(flsfile)!r} for dependencies")
            with flsfile.open() as fh:
                for line in fh:
                    if m := pattern.search(line):
                        yield m.groupdict()["file"]
        pattern = re.compile(
            r"""^\s+"(?P<file>.*?)"\s+(\d+)\s+(\d+)\s+([a-f0-9]+)\s+"([^"]*)"\s+$"""
        )
        if (fdbfile := texfile.parent / Path(f"{texfile.stem}.fdb_latexmk")).exists():
            logger.debug(f"{str(texfile)!r}: Found {str(fdbfile)!r} for dependencies")
            with fdbfile.open() as fh:
                for line in fh:
                    if m := pattern.search(line):
                        yield m.groupdict()["file"]

    #
    # Loop over all given/found tex files
    #
    for texfile in map(Path, args.texfiles):
        #
        # Get the --outdir in order
        #
        outdir_remove_after = False
        if args.inplace:
            if args.outdir:
                logger.warning(f"Ignore --outdir {args.outdir!r} as --inplace is given")
            outdir = Path(texfile).parent
        elif args.outdir:
            outdir = Path(args.outdir)
            if outdir.exists():
                if args.force:
                    shutil.rmtree(str(outdir))
                    logger.warning(f"🗑️ Removed existing --outdir {str(outdir)!r}")
                else:
                    logger.critical(
                        f"--outdir {str(outdir)!r} exists. Remove it or add --force."
                    )
                    sys.exit(1)
            if not outdir.exists():
                logger.info(f"Creating --outdir {args.outdir!r}")
                try:
                    outdir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    logger.critical(f"Couldn't create --outdir {args.outdir!r}: {e!r}")
                    sys.exit(1)
        else:
            outdir = Path(tempfile.mkdtemp(prefix=f"latex-flatten-"))
            outdir_remove_after = True

        def put_next_to_texfile(path, name=None):
            path = Path(path)
            if name is None:
                name = path.name
            is_texfile = path.resolve() == texfile.resolve()
            if not path.is_absolute() and not is_texfile:
                path = texfile.parent / path
            try:
                target = outdir / name
                if args.copy or is_texfile:
                    shutil.copy(str(from_ := path), str(target))
                    logger.info(f"🖇️ Copied {str(from_)!r} to {str(target)!r}")
                else:
                    # TODO: relative absolute target path might be more elegant
                    os.symlink(str(from_ := path.resolve()), str(target))
                    logger.info(f"🔗 Symlinked {str(from_)!r} to {str(target)!r}")
            except shutil.SameFileError as e:
                return None
            except Exception as e:
                logger.error(
                    f"💥 Couldn't {'copy' if args.copy else 'link'} {str(path)!r} next to {texfile.name!r}: {e!r}"
                )
                return False
            return True

        # all found, unique input files, including global LaTeX ones
        inputFiles = set()
        inputFilesResolved = set()
        for inputfile in map(Path, readInputFiles(texfile)):
            if (resolved := inputfile.resolve()) not in inputFilesResolved:
                inputFiles.add(inputfile)
            inputFilesResolved.add(resolved)
        logger.debug(f"{str(texfile)!r} has {len(inputFiles)} dependent files in total")
        if logger.getEffectiveLevel() < logging.DEBUG - 10:
            logger.debug(inputFiles)

        if not inputFiles:
            logger.warning(
                f"No input files detected (from *.fls or *.fdb_latexmk files next to {str(texfile)!r})! "
                f"Apparently, you didn't run 'latexmk' or 'pdflatex -recorder' on {str(texfile)!r}? "
                f"Continuing anyway, but the result might be unexpected."
            )

        # files to include in outdir or ZIP file
        # mapping of original input file to target name
        inputFilesToInclude = {f: f.name for f in inputFiles}

        # drop all absolute paths (those are the global TeX dependencies)
        inputFilesToInclude = {
            f: n for f, n in inputFilesToInclude.items() if not f.is_absolute()
        }
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(
                f"{str(texfile)!r}: dependencies inclusion list after dropping absolute paths:\n{inputFilesToInclude}"
            )

        def dont_include_file(path=None, glob=None):
            toremove = set()
            if path is not None:
                path = Path(path)
                if not path.is_absolute():
                    path = texfile.parent / path
            for inputfile in inputFilesToInclude:
                inputfile_ = inputfile
                if not inputfile_.is_absolute():
                    inputfile_ = texfile.parent / inputfile_
                if path is not None:
                    if inputfile_.resolve() == path.resolve():
                        toremove.add(inputfile)
                try:
                    if Path(inputfile).match(glob):
                        toremove.add(inputfile)
                except Exception:
                    pass
            if path and not toremove:
                logger.debug(
                    f"Instruction to not include {str(path)!r} explicitly didn't change anything."
                )
            for f in toremove:
                logger.debug(
                    f"Remove {str(f)!r} from dependency inclusion list for {str(texfile)!r}"
                )
                del inputFilesToInclude[f]

        if not args.keep_other_files:
            for pattern in (
                "*.aux *.log *.toc *.fdb_latexmk *.fls *.bbl *.blg *.fff "
                "*.lof *.lot *.ttt *.spl *.out *.bcf *.tdo *.run.xml"
            ).split():
                dont_include_file(glob=pattern)

        logger.debug(
            f"{str(texfile)!r} has {len(inputFilesToInclude)} dependent files to include"
        )
        if logger.getEffectiveLevel() < logging.DEBUG:
            logger.debug(inputFilesToInclude)

        # Make sure the texfile is actually in outdir
        put_next_to_texfile(texfile)
        dont_include_file(Path(texfile.name))

        texfile_edit = outdir / texfile.name

        logger.debug(rf"{str(texfile_edit)!r}: Flattening all \input first")
        for result in process(
            texfile=texfile_edit,
            texfiledir=texfile.parent.absolute(),
            writeout=True,
            args=args,
        ):
            if isinstance(result, Path):
                dont_include_file(result)
            elif isinstance(result, dict):
                for old, new in result.items():
                    logger.info(rf"Will include file {str(old)!r} as {new!r}")
                    inputFilesToInclude[old] = new

        logger.debug(rf"{str(texfile_edit)!r}: \input{{}}s flattened recursively")

        with texfile_edit.open("rb") as fh:
            texcode = fh.read()

        #
        # Adjust all \includegraphics{} paths
        #
        logger.info(
            rf"{str(texfile)!r}: Searching for \includegraphics{{...}} for adjusting include paths"
        )
        graphicscounter = itertools.count(start=1)
        texcode_replacements = dict()
        for match in re.finditer(
            rb"(?P<fullline>^.*?(?P<includegraphicscmd>\\includegraphics\s*(?:\[[^\]]+\])?\s*\{\s*(?P<includegraphicspath>[^}]+)\s*\}).*?$)",
            texcode,
            flags=re.MULTILINE,
        ):
            fullline = match.groupdict()["fullline"]
            includegraphicscmd = match.groupdict()["includegraphicscmd"]
            includegraphicspath = match.groupdict()["includegraphicspath"].strip()
            logger.debug(f"""{match.span("includegraphicscmd") = }""")
            logger.debug(
                f"""{texcode[match.span("includegraphicscmd")[0]:match.span("includegraphicscmd")[1]] = }"""
            )
            logger.debug(f"""{match.groupdict()["includegraphicscmd"] = }""")
            if re.search(rb"^\s*%", fullline):  # skip comments
                logger.debug(
                    rf"{str(texfile)!r}: Ignore commented \includegraphics line {fullline.decode()!r}"
                )
                # console.log(Syntax(fullline.decode(), lexer="latex"))
                continue
            graphicsnumber = next(graphicscounter)
            logger.info(
                rf"{str(texfile)!r}: Found \includegraphics line #{graphicsnumber}"
            )
            if logger.getEffectiveLevel() < logging.INFO:
                present_latex(fullline)
            # console.log(Syntax(fullline.decode(), lexer="latex"))
            includegraphicspath = Path(includegraphicspath.decode(errors="ignore"))
            if not includegraphicspath.suffixes:
                logger.warning(
                    rf"\includegraphics path {str(includegraphicspath)!r} has no suffix. This might cause issues."
                )
            if args.sequential_figures:
                includegraphicspath_new = args.sequential_figures(graphicsnumber)
                # add old suffix
                includegraphicspath_new = "".join(
                    [includegraphicspath_new] + includegraphicspath.suffixes
                )
                # included files should be included with new name
                inputFilesToInclude[includegraphicspath] = includegraphicspath_new
                logger.info(
                    f"Will include graphic {str(includegraphicspath)!r} as {str(includegraphicspath_new)!r}"
                )
            else:
                # included files should be included as-is
                # TODO: encoding weirdness might happen
                includegraphicspath_new = includegraphicspath.name
                inputFilesToInclude[includegraphicspath] = includegraphicspath_new
            includegraphicscmdnew = includegraphicscmd
            # update the included path
            includegraphicscmdnew = batch_replace(
                includegraphicscmd,  # we operate within the 'includegraphicscmd' group
                offset=match.span("includegraphicscmd")[0],
                replacements={
                    match.span("includegraphicspath"): includegraphicspath_new.encode(
                        errors="ignore"
                    )
                },
            )
            if args.hide_figures:
                # comment it out
                includegraphicscmdnew = re.sub(
                    rb"(^|[\r\n])", rb"\1% ", includegraphicscmdnew
                )
            texcode_replacements[
                match.span("includegraphicscmd")
            ] = includegraphicscmdnew
            logger.info(rf"✂️  Adjusted \includegraphics line #{graphicsnumber}")
            if logger.getEffectiveLevel() <= logging.INFO:
                present_latex(
                    includegraphicscmd,
                    includegraphicscmdnew,
                    title=f"[bold]{texfile}[/bold]:\nAdjusting [code]\includegraphics{{{includegraphicspath}}}[/code]",
                )
        texcode = batch_replace(texcode, texcode_replacements)

        if args.replace_bib:
            bblfile = texfile.parent / Path(f"{Path(texfile).stem}.bbl")
            logger.debug(
                rf"{str(texfile)!r}: Replacing \bibliography{{}} with contents of the .bbl file (assumed to be {str(bblfile)!r})"
            )
            bbllinecounter = itertools.count(start=1)
            texcode_replacements = dict()
            for match in re.finditer(
                rb"(?P<fullline>^.*?(?P<bibliographycmd>\\bibliography\s*\{\s*(?P<bibliographypath>[^}]+)\s*\}).*?$)",
                texcode,
                flags=re.MULTILINE,
            ):
                fullline = match.groupdict()["fullline"]
                bibliographycmd = match.groupdict()["bibliographycmd"]
                bibliographypath = match.groupdict()["bibliographypath"]
                if re.search(rb"^\s*%", fullline):  # skip comments
                    logger.debug(
                        rf"{str(texfile)!r}: Ignore commented \bibiliography line {fullline.decode()!r}"
                    )
                    # console.log(Syntax(fullline.decode(), lexer="latex"))
                    continue
                bbllinenumber = next(bbllinecounter)
                logger.info(
                    rf"{str(texfile)!r}: Found \bibiliography line #{bbllinenumber}"
                )
                if logger.getEffectiveLevel() < logging.INFO:
                    present_latex(bibliographycmd)

                try:
                    with bblfile.open("rb") as fh:
                        bblcontent = fh.read()
                        logger.info(
                            f"Read {len(bblcontent)} bytes from {str(bblfile)!r}"
                        )
                except Exception as e:
                    logger.error(
                        rf"Couldn't replace {bibliographycmd!r} call with contents of {str(bblfile)!r}: {e!r}. "
                        rf"Maybe you need to recompile your document, e.g. with `latexmk {str(texfile)!r}`?"
                    )
                    continue
                bibliographycmdnew = batch_replace(
                    fullline,
                    offset=match.span("fullline")[0],
                    replacements={match.span("bibliographycmd"): bblcontent},
                )
                if logger.getEffectiveLevel() <= logging.INFO:
                    present_latex(
                        bibliographycmd,
                        bibliographycmdnew,
                        title=f"[bold]{texfile}[/bold]:\nAdjusting [code]\\bibliography{{{bibliographypath}}}[/code]",
                    )
                texcode_replacements[match.span("bibliographycmd")] = bblcontent

                logger.info(
                    rf"Replaced \bibiliography line #{bbllinenumber} with contents of {str(bblfile)!r}"
                )
                if args.keep_other_files:
                    dont_include_file(bblfile.name)
            texcode = batch_replace(texcode, texcode_replacements)

        with texfile_edit.open("wb") as fh:
            logger.info(f"💾 Saving {str(texfile_edit)!r}")
            fh.write(texcode)

        logger.info(
            rf"{str(texfile)!r}: Copying all local input dependencies next to {str(texfile_edit)!r}"
        )
        for inputfile, name in inputFilesToInclude.items():
            put_next_to_texfile(inputfile, name=name)

        if args.zip:
            try:
                with ZipFile(
                    str(zipfilepath := Path(f"{texfile.stem}.zip")), "w"
                ) as zipfile:
                    logger.info(f"🗃️  Writing ZIP file {str(zipfilepath)!r}")
                    logger.info(
                        f"🗃️  {str(zipfilepath)!r}: Adding {str(texfile_edit)!r}"
                    )
                    zipfile.write(str(texfile_edit), arcname=str(texfile_edit.name))
                    for inputfile, name in inputFilesToInclude.items():
                        inputfile = outdir / name
                        logger.info(
                            f"🗃️  {str(zipfilepath)!r}: Adding {str(inputfile)!r}"
                        )
                        zipfile.write(str(inputfile), arcname=name)
            except Exception as e:
                logger.error(
                    f"{str(texfile)!r}: Couldn't finish ZIP file {str(zipfilepath)!r}: {e!r}"
                )

        logger.info(f"✅ Done with {str(texfile)!r}")

        if outdir_remove_after:
            try:
                shutil.rmtree(str(outdir))
                logger.info(f"🗑️ Removed temporary --outdir {str(outdir)!r}")
            except Exception as e:
                logger.error(
                    f"Couldn't remove temporary --outdir {str(outdir)!r}: {e!r}"
                )
        else:
            try:
                _outdir = outdir.resolve()
                _outdir = outdir.relative_to(".")
                _outdir = outdir.relative_to(".", walk_up=True)
            except Exception:
                pass
            logger.info(
                f"Have a look into {str(_outdir)!r} and try to compile {texfile_edit.name!r} there (e.g. with `latexmk`)"
            )


if __name__ == "__main__":
    cli()
