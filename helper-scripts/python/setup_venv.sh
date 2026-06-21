#! /bin/bash

source ./project-vars.sh


if [ -z "$BASH_VERSION" ]
then
    echo "This script requires (assumes) BASH and BASH only."
    exit 1
fi

# DIE On simple error
set -e


THIS_FILE=`realpath ${BASH_SOURCE[0]}`
if [ ! -f ${THIS_FILE} ]
then
    printf "Cannot find file: %s" ${THIS_FILE}
    exit 1
fi
THIS_DIR=`dirname ${THIS_FILE}`

VENV_DIR=${THIS_DIR}/venv
rm -rf ${VENV_DIR}

python3 -m venv ${VENV_DIR}

function venv_activate()
{
    source ${VENV_DIR}/bin/activate
}

export -f venv_activate

venv_activate
hash -r

python -m pip install -r ./requirements.txt
