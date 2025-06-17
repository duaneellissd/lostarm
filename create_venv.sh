#! /bin/bash


tmp=`realpath ${BASH_SOURCE[0]}`
HERE=`dirname $tmp`
VENV_DIR=${HERE}/venv

rm -rf $VENV_DIR

python3 -m venv ${VENV_DIR}

local_modules_dir=${HERE}/tools/py_modules

tmp=`ls -d ${VENV_DIR}/lib/python*/site-packages`

echo "${local_modules_dir}" >  $tmp/local_modules.pth



