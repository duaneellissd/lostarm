#! /bin/bash
# The intent is you source this file when you wish to use python.
# and want to setup a VENV



if [ "$PROJECT_SETTINGS_SH" == "" ]
then
    printf "Sorry, something is wrong\n"
    printf "Did you source 'project_settings.sh' yet?\n"
    exit 1
fi

# this file
tmp1="$PROJ_ROOT_DIR/python_settings.sh"
tmp2=`realpath ${BASH_SOURCE[0]}`
if [ "$tmp1" != "$tmp2" ]
then
    echo "Something seems wrong"
    echo "tmp1=$tmp1"
    echo "tmp2=$tmp2"
    exit 1
fi

if [ "$PYTHON_SETTINGS_SH" == "$tmp1" ]
then
    echo "Already included: $PYTHON_SETTINGS_SH"
    return
fi

set -x
provide_default PROJ_PYTHON3_EXE   `which python3`
set +x
echo PROJ_PYTHON3_EXE=${PROJ_PYTHON3_EXE}

exit 0

provide_default PYTHON_SETTINGS_SH  "$tmp1"
provide_default LOSTARM_VENV_DIR "$PROJ_ROOT_DIR/.venv"

must_be_defined LOSTARM_PYTHON_EXE

function setup_venv{
    $PROJ_PYTHON_DIR/
