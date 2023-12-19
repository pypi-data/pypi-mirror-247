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
from io import BytesIO
import platform

from docopt import docopt
from PIL import Image
import pytesseract

from ocr_shell import __version__

is_mac = platform.system() == 'Darwin'

if is_mac:
    from AppKit import NSPasteboard, NSTIFFPboardType
else:
    import win32clipboard


def main():
    options = docopt(__doc__, version=__version__)
    fp = options['<file>'] or '-'
    if fp == '-':
        fp = get_image_data()
        if fp is None:
            print("No image data found", file=sys.stderr)
            return 1
    print(ocr(fp))

def ocr(fp):
    image = Image.open(fp)
    text = pytesseract.image_to_string(image)
    return text.strip()

def get_image_data_mac():
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard_data = pasteboard.dataForType_(NSTIFFPboardType)
    if not pasteboard_data:
        return None
    # If there's image data on the pasteboard, convert it to a PIL Image
    tiff_data = pasteboard_data.bytes().tobytes()
    return BytesIO(tiff_data)

def get_image_data_windows():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            return BytesIO(data)
        return None
    finally:
        win32clipboard.CloseClipboard()

if is_mac:
    get_image_data = get_image_data_mac
else:
    get_image_data = get_image_data_windows

if __name__ == '__main__':
    sys.exit(main())
