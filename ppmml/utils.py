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

""" This module provide ppmml utilities """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import sys
import logging
import logging.handlers
import pkg_resources
import subprocess
import shutil

def _init_log(level=logging.INFO,
              format="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
              datefmt="%y-%m-%d %H:%M:%S"):
    """ init_log - initialize log module
    logging to stderr and stdout

    Args:
      level: logging level, the default value is logging.INFO
      format: logging format
      datefmt: date format
    """
    logger = logging.getLogger()
    if len(logger.handlers) > 0:
        return
    formatter = logging.Formatter(format, datefmt)
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def _is_jar_excluded(jar_name, excludes):
    """ test if jar is excluded from classpath

    Args:
    jar_name: string, jar name
    excludes: set of string, exclusion jar names
    """
    for exclusion in excludes:
        if exclusion in jar_name:
            logging.debug("exclude jar {}, {}".format(jar_name, exclusion))
            return True
    return False


def _is_jar_includes(jar_name, includes):
    """ test if jar includes in classpath

    Args:
    jar_name: string, jar name
    includes: set of string, jar names
    """
    for include_tag in includes:
        if include_tag in jar_name:
            logging.debug("include jar {}, {}".format(jar_name, include_tag))
            return True
    return False

def _get_classpath(excludes=None, includes=None):
    """ get classpath by listing resources

    Args:
        excludes: set of string, exclusion jar names
        includes: set of string, including jar names
    """
    jars = []
    resources = pkg_resources.resource_listdir("ppmml.resources", "")
    for resource in resources:
        if (resource.endswith(".jar") and
            (includes is None or _is_jar_includes(resource, includes)) and
            (excludes is None or not _is_jar_excluded(resource, excludes))):
                jars.append(pkg_resources.resource_filename("ppmml.resources", resource))
    if len(jars) > 0:
        classpath = os.pathsep.join(jars)
    else:
        classpath = ""
    return classpath


def _exec_java(classpath, main_class, args=None):
    """ a utility function to start a java subprocess

    TODO: check java must be 1.8 version
    """
    cmd = ["java", "-cp", classpath, main_class]
    if (args is not None) and len(args) > 0:
        cmd.extend(args)
    cmd = ' '.join(cmd)
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        logging.error("ppmml start java process failed "
          "with exception")
        raise e


def _normalize_path(path):
    """ normalize to absolute path
    """
    abspath = os.path.abspath(path)
    return abspath


def _ensure_path(file_path):
    """ make parent dir if it doesn't exist
    """
    parent = os.path.dirname(file_path)
    if not os.path.exists(parent):
        os.makedirs(parent)


def _check_path(path):
    """ make parent dir if it doesn't exist
    """
    if not os.path.exists(path):
        raise ValueError("path doesn't exist: {}".format(path))


