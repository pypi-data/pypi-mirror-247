from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'Tubes'

this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / 'README.md').read_text()

# Setting up
setup(
    name="Tugas",
    version=VERSION,
    author="SeladaKeju",
    author_email="<rizqiadit2430@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/SeladaKeju/Tugas',
    packages=find_packages(),
    license='MIT',
    install_requires=[],
    keywords=['Tubes'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)