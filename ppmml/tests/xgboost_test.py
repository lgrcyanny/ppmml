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
import xgboost

import ppmml
from ppmml import utils
from ppmml.tests.test_utils import TestData

class XGBoostConverterTest(unittest.TestCase):
    """ Test XGBoost Converter
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

    def _gen_fmap_file(self, features, fout):
        """ generate xgboost fmap file
        """
        with open(fout, 'w+') as f:
            for i, feature in enumerate(features):
                f.write("{0}\t{1}\tq\n".format(i, feature))

    def test_xgboost_classifier(self):
        """ test converting xgboost model
        """
        classifier = xgboost.XGBClassifier(max_depth=6,
            learning_rate=0.1, n_estimators=10,
            silent=True, objective='"multi:softmax"')
        classifier.fit(self.data.X, self.data.y)

        fmap_output = os.path.join(self.data.base_path, "xgboost_fmap.txt")
        self._gen_fmap_file(self.data.features, fmap_output)

        model_output = os.path.join(self.data.base_path, "xgboost_classifier.model")
        classifier._Booster.save_model(model_output)
        self.assertTrue(os.path.exists(model_output))

        pmml_output = os.path.join(self.data.base_path, "xgboost_classifier.pmml")
        ppmml.to_pmml(
            model_input=model_output,
            pmml_output=pmml_output,
            model_type='xgboost',
            schema_input=fmap_output,
            options={'compact': 'True', 'target-name': 'y'})
        self.assertTrue(os.path.exists(pmml_output))

        # validate pmml file
        data_output = os.path.join(self.data.base_path, "xgboost_classifier.csv")
        ppmml.predict(pmml_output, self.data.test_data_input, data_output)
        self.assertTrue(os.path.exists(data_output))

        with self.assertRaises(ValueError):
            # test invalid options
            ppmml.to_pmml(
                model_input=model_output,
                pmml_output=pmml_output,
                model_type='xgboost',
                schema_input=fmap_output,
                options={'invalid_option': 'invalid_option'})


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(XGBoostConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)