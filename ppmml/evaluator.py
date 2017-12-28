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
"""Evaluate pmml file, it's a wrapper of jpmml-evaluator-example"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from ppmml import utils

utils._init_log()
MAIN_CLASS = "org.jpmml.evaluator.EvaluationExample"
PMML_INPUT_OPTION = "--model"
DATA_INPUT_OPTION = "--input"
DATA_OUTPUT_OPTION = "--output"
ADVANCED_OPTIONS = {
    # CSV cell separator character
    'separator': '--separator',
    # Permit missing input field columns, default false
    'sparse': '--sparse',
    # copy all columns from input CSV file to output CSV file, defaut true
    'copy-columns': '--copy-columns'
}
CLASSPATH_INCLUDES = ["jpmml-evaluator-example"]

def predict(pmml_input, data_input, data_output, options=None):
    """ Make predictions with pmml file
    it's a simple wrapper of jpmml-evaluator-example for pmml model validation
    More usage about jpmml-evaluator: https://github.com/jpmml/jpmml-evaluator

    Args:
        pmml_file: string, pmml file input path
        data_input: string, input csv file path
        data_output: string, output csv file path
        options: dictionary, advanced options
    """
    run_args = []
    # prepare run args
    pmml_file_path = utils._normalize_path(pmml_input)
    csv_input_path = utils._normalize_path(data_input)
    csv_output_path = utils._normalize_path(data_output)
    utils._check_path(pmml_file_path)
    utils._check_path(csv_input_path)
    utils._ensure_path(csv_output_path)
    logging.info("Starting to make predictions of "
        "pmml file: {}, "
        "data_input: {}, data_output: {}"
        .format(pmml_file_path, csv_input_path, csv_output_path))
    run_args.extend([PMML_INPUT_OPTION, pmml_file_path])
    run_args.extend([DATA_INPUT_OPTION, csv_input_path])
    run_args.extend([DATA_OUTPUT_OPTION, csv_output_path])

    if (options is not None) and (len(options) > 0):
        for opt, value in options.items():
            if opt in ADVANCED_OPTIONS.keys():
                if (isinstance(value, bool) and value) or (value == 'True'):
                    run_args.extend([ADVANCED_OPTIONS[opt]])
                else:
                    run_args.extend([ADVANCED_OPTIONS[opt], str(value)])
            else:
                raise ValueError("Unsupported option {}, "
                    "supported options are: {}".format(opt,
                        ADVANCED_OPTIONS.keys()))
    classpath = utils._get_classpath(includes=CLASSPATH_INCLUDES)
    utils._exec_java(classpath, MAIN_CLASS, args=run_args)
    logging.info("Successfully generate predictions to path: {}".format(csv_output_path))

