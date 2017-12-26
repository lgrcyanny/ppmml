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
"""BaseConverter to convert models file to pmml files
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import logging
from ppmml import utils

class BaseConverter(object):
    """ convert model file to pmml file
    """

    def __init__(
        self, main_class, input_option, output_option,
        schema_option=None,
        classpath_excludes=None, advanced_option_keys=None):
        utils._init_log()
        self.main_class = main_class
        self.input_option = input_option
        self.output_option = output_option
        self.classpath = utils._get_classpath(classpath_excludes)
        self.advanced_option_keys = advanced_option_keys
        self.schema_option = schema_option

    def _prepare_base_args(self, model_input, pmml_output):
        """ prepare java input args
        """
        model_input_path = utils._normalize_path(model_input)
        pmml_output_path = utils._normalize_path(pmml_output)
        utils._check_path(model_input_path)
        utils._ensure_path(pmml_output_path)
        run_args = [self.input_option, model_input_path,
            self.output_option, pmml_output_path]
        return run_args

    def _prepare_advanced_args(self, options=None):
        """ generate advanced args base on user options
        """
        args = []
        if options is None:
            return args
        for opt, value in options:
            if opt in self.advanced_option_keys.keys():
                args.extend([self.advanced_option_keys[opt], value])
            else:
                advanced_option_keys_str = ','.join(self.advanced_option_keys.keys())
                raise ValueError("Unsupported option, "
                    "supported options: [{}], your option is: {}".format(
                        self.advanced_option_keys_str, opt))
        return args

    def _prepare_schema_args(self, schema_input):
        """ prepare schema args
        """
        args = []
        if schema_input is not None:
            utils._check_path(schema_input)
            args = [self.schema_option, schema_input]
        return args

    def to_pmml(self, model_input, pmml_output, schema_input=None, options=None):
        """ to_pmml file
        """
        logging.info("Startint to convert model file {} to pmml file {} "
            "with schema {} and options: {}"
            .format(model_input, pmml_output, schema_input, str(options)))
        run_args = self._prepare_base_args(model_input, pmml_output)
        advanced_args = self._prepare_advanced_args(options)
        schema_args = self._prepare_schema_args(schema_input)
        run_args.extend(advanced_args)
        run_args.extend(schema_args)
        utils._exec_java(self.classpath, self.main_class, run_args)
        logging.info("Successfully generate pmml file: {}".format(pmml_output))

