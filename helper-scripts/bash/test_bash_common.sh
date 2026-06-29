#! /bin/bash

tmp=$(realpath "${BASH_SOURCE[0]}")
tmp=$(dirname "$tmp")
export PROJ_ROOT_DIR="$tmp"

source "${PROJ_ROOT_DIR}/bash-common.sh"

must_be_defined PROJ_ROOT_DIR
must_be_defined FOOBAR
provide_default FOOBAR 1234

echo "DONE, inspect with your eyeballs"
exit 0
