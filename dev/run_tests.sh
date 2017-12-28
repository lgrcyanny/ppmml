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

WORK_DIR=$(cd `dirname $0`;pwd)
PROJECT_DIR=$(cd $WORK_DIR/..;pwd)
PYTHON_BASE=$PROJECT_DIR/ppmml
PYTHON_RUN_TESTS=$WORK_DIR/run_tests.py

function run_tests() {
    cd $PROJECT_DIR
        python $PYTHON_RUN_TESTS "$@"
    cd -
}

function main() {
    run_tests "$@"
}

main "$@"