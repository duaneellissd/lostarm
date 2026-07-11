#! /bin/bash
set -e

echo "BEGIN: ${BASH_SOURCE[0]}"
tmp=`realpath ${BASH_SOURCE[0]}`
tmp=`dirname $tmp`
if [ "$PROJ_ROOT_DIR" == "" ]
then
    source ${tmp}/project_settings.sh
fi

source ${PROJ_ROOT_DIR}/helper-scripts/bash/bash_common.sh

rm -rf ${LOSTARM_VENV_DIR}

bash ${PROJ_PYTHON_DIR}/create_venv.sh

echo "END: ${BASH_SOURCE[0]}"
