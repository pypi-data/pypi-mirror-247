# argparsemd

A package that extends Python `argparse.ArgumentParser` with Markdown help.

## intro

For documentation purposes it might be useful to be able to produce the help
text of a python program in markdown format.

This package implements a subclass of `argparse.ArgumentParser` and automatically adds a `-md` option that will produce the same information as the `-h` option but as markdown.  The `-h` keeps on working as before.

An example is shown in the section [example](#example)

## requirements

No external requirements but be aware that this only has been tested with Python 3.11.

It might work with earlier or later versions but because the `argparse` package doesn't lend
itself very well to subclassing without rewriting hundreds of lines of code, your mileage
may vary. 

## warning

This package does not have a test-suite and may break everything you touch. Use at your own risk.

## installation

Install it directly from PyPi

```
pip install argparsemd
```

or alternatively, download it from GitHub

```
git clone https://github.com/varkenvarken/argparsemd.git
cd argparsemd
python setup.py install
```

## example


```python
from argparsemd import ArgumentParserMD

parser = ArgumentParserMD(description="Do nothing but showcase markdown help")
parser.add_argument(
    "-f",
    "--filename",
    default="sample.png",
    help="Output filename. use - for stdout.",
)
parser.add_argument("--width", type=int, default=400, help="Width in pixels")
parser.add_argument(
    "--height",
    type=int,
    default=200,
    help="Height in pixels",
)
parser.add_argument(
    "-c",
    "--character",
    action="store_true",
    default=False,
    help="Height and width are in character units",
)
args = parser.parse_args()
```

If you save this as `pyprog.py` and call that with `python myprog -md`,
his will result in the following markdown output:

```
    # myprog.py:

    ```

    usage: myprog.py [-h] [-md] [-f FILENAME] [--width WIDTH] [--height HEIGHT] [-c]

    ```

    Do nothing but showcase markdown help

    ## options:
    - **-h**, **--help** 

    show this help message and exit

    - **-md** 

    print Markdown-formatted help text and exit.

    - **-f**, **--filename** [sample.png]

    Output filename. use - for stdout.

    - **--width**:int [400]

    Width in pixels

    - **--height**:int [200]

    Height in pixels

    - **-c**, **--character** [False]

    Height and width are in character units
```

Which in a preview will show up as:

# myprog.py:

```

usage: myprog.py [-h] [-md] [-f FILENAME] [--width WIDTH] [--height HEIGHT] [-c]

```

Do nothing but showcase markdown help

## options:
- **-h**, **--help** 

  show this help message and exit

- **-md** 

  print Markdown-formatted help text and exit.

- **-f**, **--filename** [sample.png]

  Output filename. use - for stdout.

- **--width**:int [400]

  Width in pixels

- **--height**:int [200]

  Height in pixels

- **-c**, **--character** [False]

  Height and width are in character units