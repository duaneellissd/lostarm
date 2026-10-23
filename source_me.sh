#! /bin/bash

# Where is this file Located?
tmp=`realpath "${BASH_SOURCE[0]}"`
dtmp=`dirname "${tmp}"`

# We need to set the PROJ_ROOT_DIR 
if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    # Not set - then set it.
    export PROJ_ROOT_DIR="${dtmp}"
else
    # If already set make sure it matches
    if [ "${PROJ_ROOT_DIR}" != "${dtmp}" ]
    then
	printf "PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
	printf "     expected=%s\n" "${dtmp}"
	printf "not consistent, please fix\n"
	exit 1
    fi
fi
export PROJ_ROOT_DIR

# We expect to find our helpers here.
expected="${PROJ_ROOT_DIR}/proj-helper-scripts"
if [ x"${PROJ_HELPER_DIR}" == x"" ]
then
   export PROJ_HELPER_DIR="${expected}"
else
    if [ "${PROJ_HELPER_DIR}" != "${expected}" ]
    then
	printf "  PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
	printf "PROJ_HELPER_DIR=%s\n" "${PROJ_HELPER_DIR}"
	printf "       expected=%s\n" "${expected}"
	printf "not consistent, please fix\n"
	exit 1
    fi
fi
export PROJ_HELPER_DIR
src_me="${PROJ_HELPER_DIR}/source_me.sh" ]
if [ ! -f ${src_me} ]
then
    printf "%s: No such file or directory\n" "${src_me}"
    exit 1
fi
source "${PROJ_HELPER_DIR}/source_me.sh"

# Now, execute our python setup scrip.
bash "${PROJ_ROOT_DIR}/python_setup.sh"

