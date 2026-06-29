#! /bin/bash


# 
activate_sh=${LOSTARM_VENV_DIR}/bin/activate
if [ ! -f ${activate_sh} ]
then
    rm -rf ${LOSTARM_VENV_DIR}
    ${LOSTARM_PYTHON_EXE} -m venv ${LOSTARM_VENV_DIR}
fi
source ${activate_sh}
