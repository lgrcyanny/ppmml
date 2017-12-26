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
"""This module for testing tensorflow converter
"""
import os
import sys
import logging
import numpy as np
import pandas as pd
import shutil
import tempfile
import unittest

import tensorflow as tf
from tensorflow.contrib.learn import LinearClassifier
from tensorflow.contrib.learn import DNNClassifier
from tensorflow.contrib.learn import RunConfig
from tensorflow.contrib.layers import one_hot_column
from tensorflow.contrib.layers import real_valued_column
from tensorflow.contrib.layers import sparse_column_with_keys
from tensorflow.contrib.layers.python.layers.feature_column import _OneHotColumn
from tensorflow.contrib.layers.python.layers.feature_column import _RealValuedColumn
from tensorflow.contrib.layers.python.layers.feature_column import _SparseColumnKeys
from tensorflow.contrib.learn.python.learn.utils.input_fn_utils import InputFnOps

import ppmml
from ppmml import utils
from ppmml.converter import to_pmml
from ppmml.evaluator import predict
from ppmml.tests.test_utils import TestData

def _export_tf_model(estimator, serving_input_fn, model_output_path):
    """ export tensorflow model
    """
    savemodel_dir = estimator.export_savedmodel(tempfile.mkdtemp(),
        serving_input_fn = serving_input_fn, as_text = True)
    savemodel_dir = savemodel_dir.decode("UTF-8")

    if(os.path.isdir(model_output_path)):
        shutil.rmtree(model_output_path)
    shutil.move(savemodel_dir, model_output_path)


def _dnn_feature_columns(feature_columns):
    """ generate dnn feature columns
    """
    dnn_columns = []
    for col in feature_columns:
        dnn_col = real_valued_column(col, dtype = tf.float64)
        if isinstance(col, _SparseColumnKeys):
            dnn_columns.append(one_hot_column(dnn_col))
        else:
            dnn_columns.append(dnn_col)
    return dnn_columns


def _input_fn(df, cont_feature_columns, cat_feature_columns, label_column):
    """ tensorflow estimator input function

    Args:
        df: pandas dataframe
        cont_feature_columns: list of string, numeric column names
        cat_feature_columns: list of string, category column names
    """
    cont_features = {}
    for col in cont_feature_columns:
        cont_features[col] = \
            tf.constant(df[col].values, dtype = tf.float64, shape = [df[col].size, 1])

    cat_features = {}
    for col in cat_feature_columns:
        cat_features[col] = \
            tf.constant(df[col].values, dtype = tf.string, shape = [df[col].size, 1])
    features = dict(list(cont_features.items()) + list(cat_features.items()))
    label = tf.constant(df[label_column].values, shape = [df[label_column].size, 1])
    return features, label


def _serving_input_fn(cont_feature_columns, cat_feature_columns):
    """ tensorflow estimator serving input function

    Args:
        cont_feature_columns: list of string, numeric column names
        cat_feature_columns: list of string, category column names
    """
    cont_features = {}
    for col in cont_feature_columns:
        cont_features[col] = \
            tf.placeholder(dtype = tf.float64, shape = [None, 1], name = col)

    cat_features = {}
    for col in cat_feature_columns:
        cat_features[col] = \
            tf.placeholder(dtype = tf.string, shape = [None, 1], name = col)
    feature_placeholders = \
        dict(list(cont_features.items())+ list(cat_features.items()))
    features = {column: tensor for column, tensor in feature_placeholders.items()}
    label = None
    return InputFnOps(features, label, feature_placeholders)


class TensorflowConverterTest(unittest.TestCase):
    """ Test Tensorflow Converter

    Testing steps:
        1. generate tensorflow model
        please refer to
        https://github.com/jpmml/jpmml-tensorflow/blob/master/src/test/resources/main.py
        2. convert to pmml file
    """

    @classmethod
    def setUpClass(self):
        """ setup test env
        """
        tf.logging.set_verbosity(tf.logging.INFO)
        self.estimator_conf = RunConfig(num_cores = 1, tf_random_seed = 42)
        self.data = TestData()

    @classmethod
    def tearDownClass(self):
        """ clean testing data
        """
        self.data.clean()

    def _iris_dnn_features(self):
        """ get iris dnn features
        """
        return _dnn_feature_columns(self.data.features)

    def _generate_tf_model(self, estimator, model_output_path):
        iris_df = self.data.df
        iris_feature_columns = self.data.features
        def __iris_input_fn():
            return _input_fn(iris_df, iris_feature_columns, [], label_column="y")

        def __iris_serving_input_fn():
            return _serving_input_fn(iris_feature_columns, [])

        estimator.fit(input_fn = __iris_input_fn, max_steps = 10)
        _export_tf_model(estimator, __iris_serving_input_fn, model_output_path)

    def test_dnn_classifier(self):
        """ test converting DNNClassifier model
        """
        algorithm_name = "dnn_classifier"
        model_output = os.path.join(self.data.base_path, "{}".format(algorithm_name))
        classifier = DNNClassifier(
            hidden_units = [4 * 3, 2 * 3],
            feature_columns = self._iris_dnn_features(),
            n_classes = 3, optimizer = tf.train.AdamOptimizer,
            config = self.estimator_conf)
        self._generate_tf_model(classifier, model_output)
        self.assertTrue(os.path.exists(model_output))

        pmml_output = os.path.join(self.data.base_path, "{}.pmml".format(algorithm_name))
        ppmml.to_pmml(
            model_input=model_output,
            pmml_output=pmml_output,
            model_type='tensorflow')
        self.assertTrue(os.path.exists(pmml_output))

        # validate pmml file
        data_output = os.path.join(self.data.base_path, "{}.csv".format(algorithm_name))
        ppmml.predict(pmml_output, self.data.test_data_input, data_output)
        self.assertTrue(os.path.exists(data_output))

    def test_linear_classifier(self):
        """ test converting LinearClassifer model
        """
        algorithm_name = "linear_classifer"
        model_output = os.path.join(self.data.base_path, "{}".format(algorithm_name))
        classifier = LinearClassifier(
            feature_columns = self._iris_dnn_features(),
            n_classes = 3, optimizer = tf.train.AdamOptimizer,
            config = self.estimator_conf)
        self._generate_tf_model(classifier, model_output)
        self.assertTrue(os.path.exists(model_output))

        pmml_output = os.path.join(self.data.base_path, "{}.pmml".format(algorithm_name))
        ppmml.to_pmml(
            model_input=model_output,
            pmml_output=pmml_output,
            model_type='tensorflow')
        self.assertTrue(os.path.exists(pmml_output))

        # validate pmml file
        data_output = os.path.join(self.data.base_path, "{}.csv".format(algorithm_name))
        ppmml.predict(pmml_output, self.data.test_data_input, data_output)
        self.assertTrue(os.path.exists(data_output))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TensorflowConverterTest)
    unittest.TextTestRunner(verbosity=2).run(suite)