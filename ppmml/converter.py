#!/usr/bin/evn python
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2017 the ppmml authors. All Rights Reserved
# ppmml is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppmml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ppmml.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""Converter to convert models file to pmml files"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import logging
from ppmml import utils
from ppmml.sklearn import SklearnConverter
from ppmml.tensorflow import TensorflowConverter
from ppmml.lightgbm import LightGBMConverter
from ppmml.xgboost import XGBoostConverter
from ppmml.spark import SparkConverter
from ppmml.r import RConverter

_CONVERTER_MAPS = {
    'sklearn': SklearnConverter(),
    'tensorflow': TensorflowConverter(),
    'lightgbm': LightGBMConverter(),
    'xgboost': XGBoostConverter(),
    'spark': SparkConverter(),
    'r': RConverter()
}

def to_pmml(model_input,
            pmml_output,
            model_type='sklearn',
            schema_input=None,
            options=None):
    """ convert to pmml file
    """
    if _CONVERTER_MAPS.get(model_type) is None:
        raise ValueError("Converted for {} not supported yet".format(model_type))
    _CONVERTER_MAPS[model_type].to_pmml(model_input, pmml_output, schema_input, options)

