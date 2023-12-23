#! /usr/bin/env python
"""Toolbox for open set recognition."""
from __future__ import absolute_import

import codecs
import os
# read the contents of your README file
from os import path
from snowflakes import _version

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# get __version__ from _version.py
ver_file = os.path.join("snowflakes", "_version.py")
with open(ver_file) as f:
    exec(f.read())

DISTNAME = "snowflakes"
DESCRIPTION = "The snowflakes module makes snowflakes."
MAINTAINER = "P. Ksieniewicz"
MAINTAINER_EMAIL = "pawel.ksieniewicz@pwr.edu.pl"
URL = "https://github.com/xehivs/snowflakes"
LICENSE = "GPL-3.0"
DOWNLOAD_URL = "https://github.com/xehivs/snowflakes"
VERSION = _version.__version__
INSTALL_REQUIRES = ["numpy", "scipy"]
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
]


setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
)
