# OCR Shell

OCR Shell is a convenient command-line tool for quick and easy text extraction from images. Whether you have an image in your clipboard or a saved file, OCR Shell makes it easy to extract text without the hassle of manual handling.

## Prerequisite

### Tesseract OCR

* On Windows, you can download an installer from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract).
* On macOS, you can install Tesseract using Homebrew with the command `brew install tesseract`.

Make sure the `tesseract` is found on your executable PATH.

## Installation

To install OCR Shell, simply run:

```sh
pip install ocr-shell
```

This command will install OCR Shell and all its dependencies.

## Usage

### From Clipboard

To extract text from an image in your clipboard, just type:

```sh
$ ocr
... text found in the copied image ...
```

### From a File

OCR Shell also works with saved images. Just provide the path to the image:

```sh
$ ocr ~/Desktop/Screenshot.png
... more text extracted ...
```

## Unit Tests

```sh
$ python -m unittest discover
..
----------------------------------------------------------------------
Ran 2 tests in 0.407s

OK
```

## Contributing

Contributions to OCR Shell are welcome! Whether it's bug reports, feature requests, or code contributions, your input is valuable. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to your branch.
5. Submit a pull request.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Thanks to the Tesseract OCR team for their amazing work.
* Matt King for initial development.
* All contributors who help to improve OCR Shell.
