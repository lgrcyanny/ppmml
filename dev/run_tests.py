#!/usr/bin/env bash
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
"""This module provodes utils to run unit tests
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from os.path import dirname
import sys
import subprocess
import argparse
import logging

PROJECT_BASE = dirname(dirname(os.path.realpath(__file__)))
# add project base path to sys.path to enable import ppmml
sys.path.append(PROJECT_BASE)
from ppmml import utils

utils._init_log()
BASE_MODULE = "ppmml.tests"

def run_all_tests():
    """ run all unit tests
    """
    logging.info("Starting run all tests")
    cmd = "python -m unittest discover -s ppmml/tests -p *_test.py".format(PROJECT_BASE)
    subprocess.check_call(cmd, shell=True)


def run_single_test(module_name, method_name=None):
    """ single name
    """
    logging.info("starting to run single test of "
        "module: {}, method: {}".format(module_name, method_name))
    submodule = [BASE_MODULE, module_name]
    if method_name is not None:
        submodule.append(method_name)
    submodule = ".".join(submodule)
    cmd = "python -m unittest {}".format(submodule)
    subprocess.check_call(cmd, shell=True)


def main(args):
    """ entry point

    Args:
        args: list of string, command line args
    """
    # print(args)
    parser = argparse.ArgumentParser(prog="run_tests", description='Run ppmml unit tests')
    parser.add_argument("--module", type=str,
        default=None,
        dest="module",
        help="submodule for run single test, such as sklearn_test, default(%(default)s)")
    parser.add_argument("--method", type=str,
        dest="method",
        default=None, help="the method name to test, default(%(default)s)")
    opts = parser.parse_args(args)
    if opts.module is not None:
        run_single_test(opts.module, opts.method)
    else:
        run_all_tests()

if __name__ == "__main__":
    main(sys.argv[1:])