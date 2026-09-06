#! /bin/bash
# The intent is you source this file when you wish to use python.
# and want to setup a VENV

case "${LOSTARM_VERBOSE}" in
    "true" | "false")
	echo "all is well" >> /dev/null
	;;
    *)
	# default to false
	export LOSTARM_VERBOSE=false
	;;
esac
    
if [ x"$1" == x"-v" ]
then
    # remove the -v
    shift
    export LOSTARM_VERBOSE=true
fi

# Detect DOUBLE inclusion and WRONG inclusion.

# Where is this file?
this_file=`realpath ${BASH_SOURCE[0]}`
if [ x"${LOSTARM_GUARD_PYTHON_SETTINGS_SH}" == "${this_file}" ]
then
    # All is well, we are being included a second time.
    if $L

tmp_dn=`dirname  $tmp`
tmp_bn=`basename $tmp`
# Use the existing PROJ_ROOT_DIR.. it should be defined by now.
# And construct where we expect to find *THIS* file.
test_file="${PROJ_ROOT_DIR}/${tmp_bn}"
if [ x"${this_file}" != x"${test_file}" ]
then
    # This can happen if you have two copies of the project.
    # Copy (A) in directory (A)...
    #    And you have sourced the scripts in Directory(A)
    # Copy (B) in directory (B)
    #    And now you are sourcing scripts in THIS directory
    # The Variables are sort of mixed up and wrong.
    printf "Something is wrong...\n"
    printf "EXPECTED: %s\n" "${test_file}"
    printf "  ACTUAL: %s\n" "${this_file}"
    # So stop this NOW, do not proceed.
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

