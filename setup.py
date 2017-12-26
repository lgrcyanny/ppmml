#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# ###############################################################################
#
# Copyright (c) 2017 the ppmml authors. All Rights Reserved
# ppmml is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ppmml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ppmml.  If not, see <http://www.gnu.org/licenses/>.
#
# ###############################################################################
"""
This module provide ppmml setup configuration.
"""

import os
from setuptools import setup
from setuptools import find_packages

__version__ = "0.0.1"

setup(
    name = "ppmml",
    version = __version__,
    description = "Python library for converting machine learning models to pmml file",
    author ='Cyanny Liang',
    author_email='lgrcyanny@gmail.com',
    url = "https://github.com/lgrcyanny/ppmml",
    download_url = "https://github.com/lgrcyanny/ppmml/archive/" + __version__ + ".tar.gz",
    license = "GNU Affero General Public License (AGPL) version 3.0",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering"
    ],
    packages = ["ppmml", "ppmml.resources", "ppmml.tests"],
    package_data = {
        "ppmml.resources": ["*.jar"]
    },
    install_requires = [
        "scikit-learn>=0.18.0",
        "sklearn-pandas>=0.0.10",
        "xgboost>=0.6a2",
        "lightgbm>=2.0.11"
    ]
)
