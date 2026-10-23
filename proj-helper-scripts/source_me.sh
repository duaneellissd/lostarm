#! /bin/bash

if [ x"${PROJ_HELPER_DIR}" == x"" ]
then
    printf "PROJ_ROOT_DIR is not defined it is required\n"
    exit 1
fi

tmp=`realpath "${BASH_SOURCE[0]}"`
dtmp=`dirname "${tmp}"`
if [ "${PROJ_HELPER_DIR}" != "${dtmp}" ]
then
    printf "PROJ_HELPER_DIR=%s\n" "${PROJ_HELPER_DIR}"
    printf "       expected=%s\n" "${expected}"
    printf "this is not consistent, please fix\n"
    exit 1
fi

export PROJ_BASH_DIR="${PROJ_HELPER_DIR}/bash"

source ${PROJ_BASH_DIR}/source_me.sh

export PROJ_PYTHON_DIR="${PROJ_HELPER_DIR}/python"

source ${PROJ_PYTHON_DIR}/source_me.sh




