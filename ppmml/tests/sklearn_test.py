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
"""This module test sklearn converter
"""
import os
import sys
import unittest
import logging

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier

from sklearn.externals import joblib

import ppmml
from ppmml import utils
from ppmml.converter import to_pmml
from ppmml.evaluator import predict
from ppmml.tests.test_utils import TestData

class SklearnConverterTest(unittest.TestCase):
    """ Test Sklearn Converter
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

    def _to_pmml_and_validate(self, estimator, algo_name):
        """ to pmml and validate

        Args:
            estimator: sklearn estimator
            algo_name: string, the algorithm name
        """
        model_output = os.path.join(self.data.base_path, "{}.pkl.z".format(algo_name))
        pmml_output = os.path.join(self.data.base_path, "{}.pmml".format(algo_name))
        joblib.dump(estimator, model_output, compress = 9)
        ppmml.to_pmml(model_output, pmml_output, model_type="sklearn")
        self.assertTrue(os.path.exists(pmml_output))
        # validate pmml file
        data_output = os.path.join(self.data.base_path, "{}.csv".format(algo_name))
        ppmml.predict(pmml_output, self.data.test_data_input, data_output)
        self.assertTrue(os.path.exists(data_output))

    def test_decision_tree(self):
        """ test converting decision tree
        """
        tree_clf = DecisionTreeClassifier(max_depth=6)
        tree_clf.fit(self.data.X, self.data.y)
        self._to_pmml_and_validate(tree_clf, "decision_tree")

    def test_kmeans(self):
        """ test converting kmeans
        """
        cluster = KMeans(n_clusters=3, max_iter=100, random_state=42)
        cluster.fit(self.data.X)
        algo_name = "kmeans"
        self._to_pmml_and_validate(cluster, algo_name)

    def test_random_forest(self):
        """ test converting random forest
        """
        tree_clf = RandomForestClassifier(max_depth=6)
        tree_clf.fit(self.data.X, self.data.y)
        algo_name = "random_forest"
        self._to_pmml_and_validate(tree_clf, algo_name)

    def test_logistic_regression(self):
        """ test converting logistic regression
        """
        lr = LogisticRegression()
        lr.fit(self.data.X, self.data.y)
        algo_name = "logistic_regression"
        self._to_pmml_and_validate(lr, algo_name)

    def test_neural_network(self):
        """ test converting neural network
        """
        nn = MLPClassifier()
        nn.fit(self.data.X, self.data.y)
        algo_name = "neural_network"
        self._to_pmml_and_validate(nn, algo_name)

    def test_exceptions(self):
        """ test exceptions
        """
        with self.assertRaises(ValueError):
            ppmml.to_pmml("non_existent_path", "./pmml_output.pmml")


def suite():
    """ for single tests
    """
    suite = unittest.TestSuite()
    suite.addTest(SklearnConverterTest('test_neural_network'))
    return suite

if __name__ == "__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(SklearnConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite())