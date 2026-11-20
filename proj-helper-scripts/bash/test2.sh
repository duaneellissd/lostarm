#! /bin/bash

# This mostly test the various printf wrappers.

export BASH_HELPERS_FILENAME_ONLY=true

source ./printf_helpers.sh

capture_file=./actual_output/test2.out
good_file=./good_output/test2.out

rm -f "${capture_file}"

printf_with_location "hello world" >> "${capture_file}"

printf_info "This is some info" >> "${capture_file}"

BASH_HELPERS_DEBUG_LEVEL=0
verbose_printf 0 "This will be printed" >> "${capture_file}"
verbose_printf 1 "This will not be printed" >> "${capture_file}"
BASH_HELPERS_DEBUG_LEVEL=2
verbose_printf 1 "now it is printed" >> "${capture_file}"
verbose_printf 3 "Not high enough" >> "${capture_file}"
BASH_HELPERS_DEBUG_LEVEL=3
verbose_printf 3 "now it is high enough." >> "${capture_file}"

function two( )
{
    verbose_printf 0 "inside-two"
    set +x
}

function one( )
{
    verbose_printf 0 "Inside-one"
    two
}


verbose_printf 0 "at start of one two" >> "${capture_file}"
one                                    >> "${capture_file}"
verbose_printf 0 "at end of one two"   >> "${capture_file}"
# test 1 tested the fatal function.

diff "${capture_file}" "${good_file}"
if [ $? -ne 0 ]
then
    fatal_error "nested things failed"
fi
printf "TEST2: Pass\n"
exit 0
