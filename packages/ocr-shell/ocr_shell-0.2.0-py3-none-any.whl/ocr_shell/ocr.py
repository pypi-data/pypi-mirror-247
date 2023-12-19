#!/usr/bin/env python

"""
Usage:
    ocr [<file>]

Options:
    -h --help        Print this message
    --version        Print current version

<file> can be a path to an image file or `-` to indicate reading from stdin
If not specified, will read from stdin by default

"""

import sys

from docopt import docopt
from PIL import Image, ImageGrab
import pytesseract

from ocr_shell import __version__


def main():
    options = docopt(__doc__, version=__version__)
    fp = options['<file>'] or '-'
    print(ocr(fp))

def ocr(fp):
    if fp == '-':
        image = ImageGrab.grabclipboard()
        if not image:
            print("No image found on clipboard", file=sys.stderr)
            return 1
    else:
        image = Image.open(fp)
    text = pytesseract.image_to_string(image)
    return text.strip()

if __name__ == '__main__':
    sys.exit(main())
