from setuptools import setup, find_packages
from ocr_shell import __version__

setup(
    name='ocr-shell',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'docopt',
        'Pillow',
        'pytesseract',
    ],
    entry_points={
        'console_scripts': [
            'ocr=ocr_shell.ocr:main',
        ],
    },
    author='Matthew King',
    author_email='kyrrigle@gmail.com',
    description='A wrapper around tesseract that can be easily called from the command line on an image from the clipboard',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/kyrrigle/ocr-shell',
)
