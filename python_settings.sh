#! /bin/bash
# The intent is you source this file when you wish to use python.
# and want to setup a VENV
echo "BEGIN: ${BASH_SOURCE[0]}"

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
eval PYTHON_SETTINGS_SH="${tmp1}"
export PYTHON_SETTINGS_SH

if [ "${PIP_CACHE_DIR}" == "" ]
then
    # for details about this GOOGLE SEARCH the term: PIP_CACHE_DIR
    # If you have no Internet connection where you are using this
    # then step1 you might pre-download all required packages
    # then step2 Place them in this directory.
    # then step3 pip will use that directory rather then the internet.
    printf "Suggestion - set the env variable: PIP_CACHE_DIR\n" > /dev/null
fi

# EVERYTHING the lostarm scripts do with python is
# via the ENV variable: "LOSTARM_PYTHON3_EXE"
provide_default LOSTARM_PYTHON3_EXE   `which python3`
provide_default LOSTARM_VENV_DIR "$PROJ_ROOT_DIR/.venv"
must_be_defined LOSTARM_PYTHON3_EXE

echo "END: ${BASH_SOURCE[0]}"

