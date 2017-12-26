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
"""This module for R testing converter
"""
import os
import sys
import unittest
import logging
import pwd
import shutil
import tempfile

import ppmml
from ppmml import utils
from ppmml.converter import to_pmml
from ppmml.evaluator import predict


class RConverterTest(unittest.TestCase):
    """ Test R Converter
    """

    @classmethod
    def setUpClass(self):
        """ setup test env
        """
        utils._init_log()
        self.base_path = tempfile.mkdtemp(prefix='ppmml')
        self.r_model_path = \
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "rf.rds")
        utils._ensure_path(self.r_model_path)

    @classmethod
    def tearDownClass(self):
        """ clean testing data
        """
        if os.path.exists(self.base_path):
            logging.info("clean temp path: {}".format(self.base_path))
            shutil.rmtree(self.base_path)

    def test_r_converter(self):
        """ test converting r model
        """
        pmml_output = os.path.join(self.base_path, "r_model.pmml")
        ppmml.to_pmml(
            model_input=self.r_model_path,
            pmml_output=pmml_output,
            model_type='r')
        self.assertTrue(os.path.exists(pmml_output))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)