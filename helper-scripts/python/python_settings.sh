#! /bin/bash
[[ -n ${LOSTARM_GUARD_PYTHON_SETTINGS_SH:-} ]] && return
export LOSTARM_GUARD_PYTHON_SETTINGS_SH=1

# die on error.
set -e

# Where is this script?
tmp=`realpath ${BASH_SOURCE[0]}`
tmp=`dirname ${tmp}`

# get the bash helpers
source ${tmp}/bash/bash-helpers.sh

must_be_exe LOSTARM_PYTHON_EXE
must_be_defined LOSTARM_VENV_DIR

