#! /bin/bash

#! /bin/bash
# this does nothing for now.
tmp1=`realpath ${BASH_SOURCE[0]}`
tmp2=`dirname ${tmp1}`

if [ x"${PROJ_PYTHON_DIR}" != x"${tmp2}" ]
then
    printf "see: ${tmp1}\n"
    printf "PROJ_PYTHON_DIR seems wrong\n"
    printf "    actual: PROJ_PYTHON_DIR=%s\n" "${PROJ_PYTHON_DIR}"
    printf "  expected: PROJ_PYTHON_DIR=%s\n" "${tmp2}"
    exit 1
fi

#----------------------------------------
# We require a defintion of PROJ_PYTHON_EXE.
# we require this is set before we start.
#----------------------------------------
if [ x"${PROJ_PYTHON_EXE}" == x"" ]
then
    printf "PROJ_PYTHON_EXE is not defined, it is required"
    exit 1
fi

#========================================
if [ x"${PROJ_VENV_DIR}" == x"" ]
then
    echo "PROJ_VENV_DIR is not defined, it is required"
    exit 1
fi
#========================================
