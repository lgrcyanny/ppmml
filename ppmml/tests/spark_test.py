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
"""This module test spark models converter
"""
import os
import sys
import unittest
import logging
import tempfile
import shutil

import ppmml
from ppmml import utils
from ppmml.converter import to_pmml
from ppmml.evaluator import predict

class SparkConverterTest(unittest.TestCase):
    """ Test Sklearn Converter
    """

    @classmethod
    def setUpClass(self):
        """ setup test env
        """
        utils._init_log()
        self.base_path = tempfile.mkdtemp(prefix='ppmml')
        utils._ensure_path(self.base_path)
        self.test_data_path = os.path.join(self.base_path, "test.csv")

    @classmethod
    def tearDownClass(self):
        """ clean testing data
        """
        if os.path.exists(self.base_path):
            logging.info("clean temp path: {}".format(self.base_path))
            shutil.rmtree(self.base_path)

    def _run_spark(self, main_class, args):
        """ start a local spark process
        """
        excludes = ["tensorflow", "slf4j-jdk14", "jpmml-converter-1.2.6"]
        classpath = utils._get_classpath(excludes)
        utils._exec_java(classpath, main_class, args)

    def _generate_spark_models(self, main_class):
        """ generate spark models

        these java examples is packaged in ppmml-0.0.1-SNAPSHOT.jar
        the output model under base_path/{algorithm_name}_model, schema is under dir
            base_path/{algorithm_name}.json
        """
        self._run_spark(main_class, [self.base_path])

    def _generate_test_data(self, test_data_path):
        """ generate test data
        """
        self._run_spark("org.ppmml.spark.examples.GenerateTestData", [test_data_path])

    def _to_pmml_and_validate(self, algo_name):
        """ to pmml and validate

        Args:
            algo_name: string, the algorithm name
        """
        model_output = os.path.join(self.base_path, "{}_model".format(algo_name))
        schema_output = os.path.join(self.base_path, "{}.json".format(algo_name))
        pmml_output = os.path.join(self.base_path, "{}.pmml".format(algo_name))
        ppmml.to_pmml(model_output, pmml_output, schema_input=schema_output, model_type="spark")
        self.assertTrue(os.path.exists(pmml_output))
        # validate pmml file
        if not os.path.exists(self.test_data_path):
            logging.info("generate test data: {}".format(self.test_data_path))
            self._generate_test_data(self.test_data_path)
        data_output = os.path.join(self.base_path, "{}.csv".format(algo_name))
        ppmml.predict(pmml_output, self.test_data_path, data_output)
        self.assertTrue(os.path.exists(data_output))

    def test_decision_tree(self):
        """ test converting decision tree
        """
        main_class = "org.ppmml.spark.examples.DecisionTree"
        algorithm_name = "decision_tree"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)

    def test_kmeans(self):
        """ test converting kmeans
        """
        main_class = "org.ppmml.spark.examples.KMeans"
        algorithm_name = "kmeans"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)

    def test_gbdt(self):
        """ test converting gbdt classifier
        """
        main_class = "org.ppmml.spark.examples.GBTClassifier"
        algorithm_name = "gbt_classifier"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)

    def test_logistic_regression(self):
        """ test converting logistic regression
        """
        main_class = "org.ppmml.spark.examples.LogisticRegression"
        algorithm_name = "logistic_regression"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)

    def test_neural_network(self):
        """ test converting logistic regression
        """
        main_class = "org.ppmml.spark.examples.NeuralNetwork"
        algorithm_name = "neural_network"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)

    def test_neural_network(self):
        """ test converting logistic regression
        """
        main_class = "org.ppmml.spark.examples.RandomForest"
        algorithm_name = "random_forest"
        self._generate_spark_models(main_class)
        self._to_pmml_and_validate(algorithm_name)


def suite():
    """ for single tests
    """
    suite = unittest.TestSuite()
    suite.addTest(SparkConverterTest('test_kmeans'))
    return suite

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(SparkConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)