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

"""Tensorflow PMML Converter"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ppmml import utils
from ppmml.base_converter import BaseConverter

MAIN_CLASS = "org.jpmml.tensorflow.Main"
INPUT_OPTION = "--tf-input"
OUTPUT_OPTION = "--pmml-output"
CLASSPATH_EXCLUDES = ["spark", "hadoop"]

class TensorflowConverter(BaseConverter):
    """ convert tensorflow model file to pmml file
    """

    def __init__(self):
        """ init SklearnConverter
        """
        super(self.__class__, self).__init__(
            main_class=MAIN_CLASS, input_option=INPUT_OPTION,
            output_option=OUTPUT_OPTION, classpath_excludes=CLASSPATH_EXCLUDES)

