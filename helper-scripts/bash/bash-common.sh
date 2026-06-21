#! /bin/bash
#========================================
# This is a set of functions to simplify
# Writing bash scripts.
#----------------------------------------
# We attempt to follow this standard:
#  Widely used, Exported things are SNAKE_CASE_CAPS
#  Private things are snake_lower_strings.
#========================================
set -x

# do not repeat including this.
if [[ -z "${BASH_HELPERS_DONE}" ]]
then
    export BASH_HELPERS_DONE="678e5e019a79526d0fcca5e29f6e5f78"
else
    return
fi


# We require the PROJ_VARS_FILE
if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    echo "PROJ_ROOT_DIR is not set, it is required"
    exit 1
fi

#========================================
# print where this function was called from.
# this uses the "caller" function to reach up into the callstack
# Thus the first parameter is the override for how far up we go.
#========================================
function called_from () {
    echo "" >> /dev/null
#    depth=$1
#    caller 1
#    caller 2 | read -r abcLN abcF1 abcF2
#    set 
#    echo "LINENO=${LN}"
#    echo "FUNCNAME=${F1}"
#    echo "FILENAME=${F2}"
#    printf "%s:%d: (%s) " ${FILENAME} ${LINENO} ${FUNCNAME}
}
export -f called_from

#========================================
# Script is dead, print an error message and exit.
#========================================
function fatal_here() {
    local local
    local msg
    depth=$1
    msg="$2"
    called_from $depth
    printf "FATAL: %s\n" "${msg}"
    exit 1
}
export -f fatal_here


#========================================
# print a message thats it. keep going.
#========================================
function message_here() {
    local
    depth=$1
    msg="$2"
    called_from $depth
    printf "%s\n" "${msg}"
}
export -f message_here

function must_be_defined( ) {
    VARNAME="$1"

    value="${!VARNAME}"
    if [ x"${value}" == x"" ]
    then
	fatal_here 1 "${VARNAME} is not defined it is required"
    fi
    message_here 2 "Info: ${VARNAME}=${value}\n"
}
export -f must_be_defined

function provide_default() {
    VARNAME=$1
    VALUE="$2"
    old_value="${!VARNAME}"

    if [ x"${old_value}" == x"" ]
    then
	export VARNAME="${VALUE}"
    fi
    message_here 1 "Info: ${VARNAME}=${!VARNAME}"
}
export -f provide_default

