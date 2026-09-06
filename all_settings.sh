#! /bin/bash
#========================================
# This file sets all "shell variables" in one file.
#========================================
# DIE on an error.
set -e
tmp=`realpath ${BASH_SOURCE[0]}`
tmp=`realpath ${tmp}`
# If PROJ_ROOT_DIR is not set, then set it.
if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    export PROJ_ROOT_DIR="${tmp}"
fi
# Go fetch our helpers

# We use PYTHON for many things.
# And PYTHON may or may not be in your PATH.


source ${PROJ_ROOT_DIR}/project_settings.sh


# We where executed as: "bash ./filename.sh"
THIS_FILE=`realpath ${THIS_FILE}`
THIS_DIR=`dirname ${THIS_FILE}`

zero="${0}"
if [ x"${zero}" == x"bash" ]
then
    echo "All is well" > /dev/null
else
    ARG_ZERO=`realpath ${0}`

    # you must source, not execute this script.
    # this is to prevent that mistake
    # Inspired by:
    # https://superuser.com/questions/731425/bash-detect-execute-vs-source-in-a-script
    if [[ "${THIS_FILE}" == "${ARG_ZERO}" ]]; then
	>&2 echo "Don't run $0, source it"
	exit 1
    fi
fi

pushd ${THIS_DIR}
source ./project_settings.sh
source ./python_settings.sh

if [ ! -d ${LOSTARM_VENV_DIR} ]
then
    bash ./create_venv.sh
fi

# Activate our VENV.
source ${LOSTARM_VENV_DIR}/bin/activate
# return to the orig directory.
popd

