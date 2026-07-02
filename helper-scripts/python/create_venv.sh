#! /bin/bash
set -e
# We know where we are within the helper scripts directory
tmp=$(realpath "${BASH_SOURCE[0]}")
SETUP_VENV_DIR=$(dirname "$tmp")
source "${SETUP_VENV_DIR}/../bash/bash_common.sh"

must_be_defined PROJ_ROOT_DIR
must_be_defined LOSTARM_VENV_DIR
must_be_defined LOSTARM_PYTHON3_EXE

if [ -z "$BASH_VERSION" ]
then
    echo "This script requires (assumes) BASH and BASH only."
    exit 1
fi

if [ ! -x "${LOSTARM_PYTHON3_EXE}" ]
then
    printf "LOSTARM_PYTHON3_EXE=%s is not executable\n" "${LOSTARM_PYTHON3_EXE}"
    exit 1
fi

# Why this?
# 1) we want *one* script not multiple scripts to setup our VENV
# 2) The complexity of quoting things in Bash, BatchFiles and PS1 is hard.
# 3) Python is a better language to do this.
# So we have a venv_helper written in python.
"$LOSTARM_PYTHON3_EXE" "$SETUP_VENV_DIR/venv_helper.py" "${LOSTARM_VENV_DIR}"

# Make this available to others
function venv_activate()
{
    source ${VENV_DIR}/bin/activate
}

export -f venv_activate
