#! /bin/bash
# this does nothing for now.
tmp1=`realpath ${BASH_SOURCE[0]}`
tmp2=`dirname ${tmp1}`

if [ x"${PROJ_BASH_DIR}" != x"${tmp2}" ]
then
    printf "See: ${tmp1}\n"
    printf "PROJ_BASH_DIR seems wrong\n"
    printf "    actual: PROJ_BASH_DIR=%s\n" "${PROJ_BASH_DIR}"
    printf "  expected: PROJ_BASH_DIR=%s\n" "${tmp2}"
    exit 1
fi

source "${PROJ_BASH_DIR}/printf_helpers.sh"
source "${PROJ_BASH_DIR}/var_helpers.sh"
