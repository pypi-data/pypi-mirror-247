from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Basic Calculator package'
LONG_DESCRIPTION = 'A basic calcualtor package for Addition / Subtraction, Multiplication / Division, Take (n) root of a number'

# Setting up
setup(
    name="BasicCalculatorLinasPelVersion",
    version=VERSION,
    license='MIT',
    author="LinasPel (Linas Peleckas)",
    author_email="<peleckas.l@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'calculator', 'basic'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)