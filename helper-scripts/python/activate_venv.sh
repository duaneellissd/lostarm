#! /bin/bash


# 
activate_sh=${PROJ_VENV_DIR}/bin/activate
if [ ! -f ${activate_sh} ]
then
    rm -rf ${PROJ_VENV_DIR}
    ${PROJ_PYTHON_EXE} -m venv ${PROJ_VENV_DIR}
    echo "export PYTHONPATH=${PYTHONPATH}" >> ${activate_sh}
fi
source ${activate_sh}
