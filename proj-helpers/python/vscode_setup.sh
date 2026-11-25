#! /bin/bash

# this is created here to edit/test/develop these modules
# in some standalone way.



THIS_FILE=`realpath ${BASH_SOURCE[0]}`
THIS_DIR=`dirname ${THIS_FILE}`

export PROJ_PYTHON_DIR=$THIS_DIR

export PROJ_HELPERSCRIPTS_DIR=`realpath ${PROJ_PTYHON_DIR}\..`

if [ x"${PROJ_PYTHON_EXE}" == x"" ]
then
    echo "PROJ_PYTHON_EXE is not defined it is required."
    exit 1
fi
export PROJ_VENV_DIR=${PROJ_PYTHON_DIR}/.venv

${PROJ_PYTHON_EXE} ./create_venv.py
