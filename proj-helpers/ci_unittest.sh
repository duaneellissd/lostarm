#! /bin/bash


function python_test( ) {
    abs_script=`realpath "${1}"`
    dir_script=`dirname "${abs_script}"`
    file_script=`basename "${abs_script}"`

    pushd "${dir_script}"
    if [ x"${PROJ_PYTHON_EXE}" == x"" ]
    then
        echo "Variable: PROJ_PYTHON_EXE is not set, it is required"
        exit 1
    fi
    ${PROJ_PYTHON_EXE} -m unittest "${file_script}"
    if [ $? -ne 0 ]
    then
        printf "***FAIL*** %s\n" "${abs_script}"
        exit 1
    else
        printf "***FAIL*** %s\n" "${abs_script}"
    fi
    popd
}

pushd ./bash
bash ./test_all.sh
if [ $? -ne 0 ]
then
    echo "BASH tests fail."
    exit 1
fi
popd

tmp=`realpath python/modules`
export PYTHONPATH="${tmp}:${PYTHONPATH}"
python_test python/modules/projhelpers/variables/test_vars.py
python_test python/modules/projhelpers/preprocessor/test_preprocessor.py
