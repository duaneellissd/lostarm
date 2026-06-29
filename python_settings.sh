#! /bin/bash
# The intent is you source this file when you wish to use python.
# and want to setup a VENV

if [ "${PROJ_ROOT_DIR}" == "" ]
then
    printf "Sorry, PROJ_ROOT_DIR is not defined it is required\n"
    printf "Did you source 'project_settings.sh' yet?\n"
    exit 1
fi

tmp=`realpath ${BASH_SOURCE[0]}`
if [ x"${PYTHON_SETTINGS_SH}" != x"" ]
then
    if [ "${PYTHON_SETTING_SH}" == "$tmp" ]
    then
	echo "ignore dup include" >> /dev/null
	return
    else
	printf "PYTHON_SETTINGS_SH=%s\n" "$PYTHON_SETTINGS_SH"
	printf "   Does not match: %s\n" "$tmp"
	exit 1
    fi
fi
export PYTHON_SETTINGS_SH="$tmp"
provide_default HELPER_SCRIPTS_DIR "${PROJ_ROOT_DIR}/helper-scripts"
provide_default PROJ_PYTHON_DIR "${HELPER_SCRIPTS_DIR}/python"
source ${HELPER_SCRIPTS_DIR}/bash/bash-common.sh
provide_default PROJ_VENV_DIR "$PROJ_ROOT_DIR/.venv"

function setup_venv{
    $PROJ_PYTHON_DIR/
