#! /bin/bash

#
# Admittedly, this is a bad test because it requires you the
# human to inspect with your eyeballs.
#
# The solution is to run the script: 'test1.sh'
# That runs *THIS* script 5 times once for each mode below.
# The 5th time (id=4) is to test the 'usage' case
#
case "$1" in 
    "0")
        TEST_MODE=0
        echo "THIS_IS_TEST_CASE_0"
        ;;
    "1")
        TEST_MODE=1
        echo "THIS_IS_TEST_CASE_1"
        ;;
    "2")
        TEST_MODE=2
        echo "THIS_IS_TEST_CASE_2"
        ;;
    "3")
        TEST_MODE=3
        echo "THIS_IS_TEST_CASE_3"
        ;;
    *)
        printf "To test various modes, specify the mode\n"
        printf "usage: ${0} 0\n"
        printf "usage: ${0} 1\n"
        printf "usage: ${0} 2\n"
        printf "usage: ${0} 3\n"
        exit 1  
        ;;
esac

tmp="${BASH_SOURCE[0]}"

export PROJ_ROOT_DIR=$(dirname "${tmp}")

source ./printf_helpers.sh

#verbose_printf 0 "This should always print"

function three() {
    printf "Function 3\n"
    dump_bash_callstack
    if [ "$TEST_MODE" == "3" ]
    then
       fatal_error "This is a test of the fatal error at 3"
    fi
}

function two() {
    printf "Function two\n"
    dump_bash_callstack test-two
    # all function 3.
    three
    if [ "$TEST_MODE" == "2" ]
    then
       fatal_error "This is a test of the fatal error at 2"
    fi
}

function one() {
    printf "Function one\n"
    dump_bash_callstack "test-one"
    # call function 2.
    two
    if [ "$TEST_MODE" == "1" ]
    then
       fatal_error "This is a test of the fatal error at 2"
    fi
}

printf "Test function call stack and fatal error\n"
# One calls two calls three calls fatal
one
if [ "$TEST_MODE" == "0" ]
then   
    fatal_error "At main level"
fi
echo "if you see this the logic in this test file is bad/wrong"
echo "It should have caught the parameter error earlier."
exit 1
