#!/usr/bin/evn bash
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
set -e
set -o pipefail
set -u

PROJECT_DIR=$(cd `dirname $0`;pwd)
PYTHON_BASE=$PROJECT_DIR
PYTHON_RESOURCES=$PYTHON_BASE/ppmml/resources
DEPS_BASE=$PROJECT_DIR/deps
LIB_MANAGED=$DEPS_BASE/src/main/lib_managed
do_clean="False"
do_package="False"

function print_usage() {
    echo "Usage:"
    echo "  ./build.sh [options]"
    echo "Options:"
    echo "  -h|help         help guide"
    echo "  clean           clean ppmml python resources"
    echo "  package         package ppmml and generate egg package"
    echo "  deploy          deploy to pypi"
}

function clean() {
    echo "Clean ppmml resources"
    if [[ -d "$PYTHON_RESOURCES" ]];then
        set +e
        pushd $PYTHON_RESOURCES
        rm *.jar
        popd
        set -e
    fi
}

function build_jar_deps() {
    echo "Build ppmml java dependencies"
    pushd $DEPS_BASE
        mvn clean package -DskipTests
        echo "Copying jars under ${LIB_MANAGED}/*.jar to $PYTHON_RESOURCES"
        cp $LIB_MANAGED/*.jar $PYTHON_RESOURCES
    popd
}

function build_python_deps() {
    echo "Build ppmml python dependencies"
    pushd $PYTHON_BASE
        python setup.py bdist_egg
    popd
}

function package() {
    echo "Packaging ppmml..."
    if [[ "${do_clean}" = "True" ]];then
        clean
    else
        echo "clean option is disabled"
    fi
    echo "do_package ${do_package}"
    if [[ "${do_package}" = "True" ]];then
        build_jar_deps
        # build_python_deps
        echo "Successfully generate ppmml egg package under ${PROJECT_DIR}/dist"
    else
        echo "package option is disabled"
    fi
}

function main() {
    while [[ "$#" -gt 0 ]]; do
        cmd=$1
        case "${cmd}" in
            -h|help)
                print_usage
                exit 0
                ;;
            clean)
                do_clean="True"
                ;;
            package)
                do_package="True"
                ;;
            *)
                echo "unsupported options"
                print_usage
                exit 1
                ;;
        esac
        shift
    done
    set -x
    package
}

main "$@"

