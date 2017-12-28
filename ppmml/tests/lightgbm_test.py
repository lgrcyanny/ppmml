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
"""This module for testing converter
"""
import os
import sys
import unittest
import logging
import lightgbm as lgb

import ppmml
from ppmml import utils
from ppmml.converter import to_pmml
from ppmml.evaluator import predict
from ppmml.tests.test_utils import TestData

class LightGBMConverterTest(unittest.TestCase):
    """ Test LightGBM Converter
    """

    @classmethod
    def setUpClass(self):
        """ setup test env
        """
        self.data = TestData()

    @classmethod
    def tearDownClass(self):
        """ clean testing data
        """
        self.data.clean()

    def test_lightgbm_classifier(self):
        """ test converting lightgbm model
        """
        gbm = lgb.LGBMClassifier(boosting_type='gbdt',
            num_leaves=31, max_depth=6,
            learning_rate=0.1,
            n_estimators=10,
            objective='multiclass')
        gbm.fit(self.data.X, self.data.y, eval_metric='logloss', feature_name=self.data.features)

        model_output = os.path.join(self.data.base_path, "lightgbm_classifier.txt")
        gbm.booster_.save_model(model_output)
        self.assertTrue(os.path.exists(model_output))

        pmml_output = os.path.join(self.data.base_path, "lightgbm_classifier.pmml")
        ppmml.to_pmml(
            model_input=model_output,
            pmml_output=pmml_output,
            model_type='lightgbm',
            options={'compact': True, 'target-name': 'y'})
        self.assertTrue(os.path.exists(pmml_output))

        # validate pmml file
        data_output = os.path.join(self.data.base_path, "lightgbm_classifier.csv")
        ppmml.predict(pmml_output, self.data.test_data_input, data_output)
        self.assertTrue(os.path.exists(data_output))

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(LightGBMConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)