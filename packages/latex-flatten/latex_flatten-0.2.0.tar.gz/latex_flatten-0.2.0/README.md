[![PyPI version](https://badge.fury.io/py/latex-flatten.svg)](https://badge.fury.io/py/latex-flatten)
[![REUSE status](https://api.reuse.software/badge/gitlab.com/nobodyinperson/latex-flatten)](https://api.reuse.software/info/gitlab.com/nobodyinperson/latex-flatten)

# 🗜️ Flatten the file structure of a LaTeX document

## ✨ What can it do?

- replace `\input{FILE}` with contents of `FILE`
- point all `\includegraphics{PATH}` next to the .tex file
- replace `\bibliography` with contents of `.bbl` file (`--replace-bib`, needed e.g. for PLoS)
- Rename figure filenames like `fig3.pdf` (`--sequential-figures`)
- Hide figures by commenting `\includegraphics{}` (`--hide-figures`, needed for PLoS)
- copy all source files next to the LaTeX file (`--inplace`)
- modify your LaTeX file in-place (`--inplace`)
- make a new folder with the flattened LaTeX project structure (`--outdir MYDIR`)
- make a ZIP file with the flattened LaTeX project structure (`--zip`)

These steps are necessary for some Journals (e.g. Springer, PLoS, etc.). 
With `latex-flatten`, one can work flexibly on a manuscript with a nested structure and included files and flatten the project only before submission.

## 📝 TODO - Planned Features

- Have `--hide-figures` and `--sequential-figures` operate only within `figure` environments. The currently don't know whether they're manipulating an actual figure or just a random included graphic anywhere.
- Use relative (not absolute) symlinks for linking to `--outdir`.
- Find input files from `TEXINPUTS`

## ❓ Usage

You can run this tool if you have [nix](https://nixos.org) installed:

```bash
nix run gitlab:nobodyinperson/latex-flatten

# or with arguments (note the lonely double dash --)
nix run gitlab:nobodyinperson/latex-flatten -- --help
```

Otherwise, you can install it like any other Python package, e.g. with `pip` or better `pipx`:

```bash
pipx install latex-flatten

# latest development version
pipx install git+https://gitlab.com/nobodyinperson/latex-flatten
```

This installs the `latex-flatten` command:

```bash
# will operate on all *.tex documents in this folder
latex-flatten 

# specific document
latex-flatten myfile.tex 

# Make a ZIP for PLoS submission
latex-flatten --plos --zip

# Make a new folder with flattened LaTeX structure (to check compilation, etc.)
latex-flatten --outdir FLATTENED

# Make a flat ZIP from your LaTeX project
latex-flatten --zip

# Be moreo chatty, useful for debugging
latex-flatten -vvv

# Help
latex-flatten --help
```

## 🛠️ Workflow

1. Compile LaTeX successfully with `latexmk` or `pdflatex -recorder` once
2. Run this script next to (or on) the `.tex` file.

Before using `--inplace`, you should probably back up your files or git-track them to see the differences and revert in case something unexpected happens.
