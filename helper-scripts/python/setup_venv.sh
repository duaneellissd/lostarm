#! /bin/bash

# We know where we are within the helper scripts directory
tmp=$(realpath "${BASH_SOURCE[0]}")
SETUP_VENV_DIR=$(dirname "$tmp")
source "${SETUP_VENV_DIR}/../bash/bash-common.sh"

must_be_defined PROJ_ROOT_DIR
must_be_defined PROJ_VENV_DIR
must_be_defined PROJ_PYTHON_EXE

if [ -z "$BASH_VERSION" ]
then
    echo "This script requires (assumes) BASH and BASH only."
    exit 1
fi

if [ ! -x "${PROJ_PYTHON_EXE}" ]
then
    printf "PROJ_PYTHON_EXE=%s is not executable\n" "${PROJ_PYTHON_EXE}"
    exit 1
fi

# Why this?
# 1) we want *one* script not multiple scripts to setup our VENV
# 2) The complexity of quoting things in Bash, BatchFiles and PS1 is hard.
# 3) Python is a better language to do this.
# So we have a venv_helper written in python.
${PROJ_PYTHON_EXE} "${SETUP_VENV_DIR}/venv_helper.py" "${PROJ_VENV_DIR}"

# Make this available to others
function venv_activate()
{
    source ${VENV_DIR}/bin/activate
}

export -f venv_activate
