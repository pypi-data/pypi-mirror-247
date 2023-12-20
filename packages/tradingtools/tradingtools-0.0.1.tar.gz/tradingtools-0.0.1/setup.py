from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Tools for trading'
LONG_DESCRIPTION = 'Tools for trading'

# Setting up
setup(
    name="tradingtools",
    version=VERSION,
    author="OverclockedD2",
    author_email="<overclockedd2@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3"
    ]
)
