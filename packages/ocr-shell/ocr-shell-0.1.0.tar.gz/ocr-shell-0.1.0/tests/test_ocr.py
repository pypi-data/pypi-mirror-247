import unittest
from ocr_shell.ocr import ocr

class TestOCRShell(unittest.TestCase):

    def test_ocr_from_file(self):
        # Test OCR functionality from a file
        test_image_path = 'tests/sample-1.png'
        expected_text = '''OCR Shell is a convenient command-line tool for quick and easy text
extraction from images. Whether you have an image in your clipboard
or a saved file, OCR Shell makes it easy to extract text without the
hassle of manual handling.'''
        result_text = ocr(test_image_path)  # Replace with your actual function call
        self.assertEqual(result_text, expected_text)

    def test_ocr_from_clipboard(self):
        # Test OCR functionality from clipboard
        # This might be tricky depending on how you handle clipboard data
        pass

if __name__ == '__main__':
    unittest.main()
