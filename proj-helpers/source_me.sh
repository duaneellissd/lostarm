#! /bin/bash
#--------------------------------------------------
# PURPOSE OF THIS SCRIPT.
#    This REPO is/should be a SUBMODULE of another (the parent) project.
#    That project should/must:
#       A) set PROJ_ROOT_DIR to that directory.
#       B) Set the variable PROJ_HELPER_DIR to THIS directory.
#       C) Source this script to set some more variables.
#

if [ "x${BASH_VERSION}" == x"" ]
then
    printf "This does not appear to be BASH.\n"
    printf "These scripts require BASH\n"
    exit 1
fi

#==================================================
# Are we in the correct place?
#==================================================
# is PROJ_HELPER_DIR pointing at the right place?
expected=${PROJ_HELPER_DIR}/`basename "${BASH_SOURCE[0]}"`
actual=`realpath ${BASH_SOURCE[0]}`

if [ x"${expected}" != x"${actual}" ]
then
  printf "Inconsistent PROJ_HELPER_DIR setting\n"
  printf "  Actual: %s\n" "${actual}"
  printf "Expected: %s\n" "${expected}"
  exit 1
fi
#==================================================
# we are.
#==================================================

export PROJ_BASH_DIR=${PROJ_HELPER_DIR}/bash
source ${PROJ_BASH_DIR}/source_me.sh

export PROJ_PYTHON_DIR=${PROJ_HELPER_DIR}/python
source ${PROJ_PYTHON_DIR}/source_me.sh
