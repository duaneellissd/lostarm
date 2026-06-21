#! /bin/bash

tmp=`realpath ${BASH_SOURCE[0]}`
tmp=`dirname $tmp`
export PYTHON_MODULE_DIR=${tmp}/modules

export PROJ_PYTHON_EXE=`which python3`

if [[ ":$PYTHONPATH:" == *":$PYTHON_MODULE_DIR:"* ]]; then
    echo "already in path" >> /dev/null
else
    export PYTHONPATH=${PYTHON_MODULE_DIR}:${PYTHONPATH}
fi
