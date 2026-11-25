#! /bin/bash

#==================================================
# Overall concept for the package is this:
#   At the file system we look for "ci_unittest.sh" as a bash script.
#   Why BASH?  This provides uniformity, if we change this we will look for python files.
#   Why NOT BASH? (if we change, we will use python because it works on windows + linux + mac)
#   But today we are targeting bash scripts.
#
#   We only 'discover/search' *ONE* directory layer down.
#   We look for exactly the filename: "ci_unittest.sh"  # future: ci_unittest.py
#   And we execute all of these we find.
#   These scripts shall exit 0 on success.
#   These scripts shall exit NON-ZERO on error/failure.
#==================================================

# Numerous things require PYTHON make sure we know where it is.
if [ x"${PROJ_PYTHON_EXE}" == x"" ]
then
    this_script=`realpath "${BASH_SOURCE[0]}"`
    printf "%s:%s: Fatal: PROJ_PYTHON_EXE is not defined, it is required\n" "${this_script}" "${LINENO}"
    exit 1
fi

# Look one layer deep and call all of the ones we find.

for test_script in */ci_unittest.sh
do
    d_name=`dirname "${test_script}"`
    b_name=`basename "${test_script}"`

    pushd "${d_name}"
    bash  "${b_name}"
    if [ $? -ne 0 ]
    then
        printf "*** FAIL *** ${test_script}\n"
        exit 1
    else
        printf "*** PASS *** ${test_script}\n"
    fi
done

exit 0
