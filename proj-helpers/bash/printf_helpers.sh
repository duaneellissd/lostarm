#! /bin/bash
#========================================================
# this is a collection of bash functions wrapping printf.
#========================================================

# we die if there is a simple error.
set -e

function dump_bash_callstack() {
    local why
    why="$1"
    # this prints/dumps the bash script callstack.
    local i
    for (( i = ((${#FUNCNAME[@]}-1)) ; i > 0; i-- ))
    do
        filename="${BASH_SOURCE[$i]}"
        lineno="${BASH_LINENO[$i]}"
	    func="${FUNCNAME[$i]}"

        if [ x"${filename}" != x"" ]
        then
            filename=`realpath "${filename}"`
            if [ x"$BASH_HELPERS_FILENAME_ONLY" == x"true" ]
            then
                filename=`basename "${filename}"`
            fi
        fi

        if [ "${lineno}" == "0" ]
        then
            # this is the main file we are running.
            printf "%s:1:%s: - The root bash script\n" "${filename}" "${why}"
            continue
        fi
        if [ x"${func}" == x"source" ]
        then
            printf "%s:%s:%s - Sourced here\n" "${filename}" "${lineno}" "${why}"
            continue
        fi
        printf "%s:%s:%s: function: %s\n" "${filename}" "${lineno}" "${why}" "${func}"
        continue
    done
}

function param_count_check() {
    local desired
    local actual
    desired="$1"
    actual="$2"
    extra="$3"

    if [ "$desired" != "${actual}" ]
    then
	    dump_bash_callstack
	    printf "FATAL ERROR: Wrong number of parameters (extra=%s)\n" "${extra}"
	    printf "Expected %s, got %s" "${desired}" "${actual}"
	    exit 1
    fi
}

function _printf_with_location_() {
    local depth
    local msg
    depth="${1}"
    msg="${2}"
    local line
    local file
    local bname # cspell:ignore bname
    local dname
    local bdname # cspell:ignore bdname

    #echo "Depth=${depth}"
    _caller="$(caller ${depth})"
    read -r line func file <<< "$_caller"
    file=`realpath "${file}"`
    bname=`basename "${file}"`
    dname=`dirname "${file}"`
    dbname=`basename "${dname}"` # cspell:ignore dbname

    printf "%s/%s:%s: %s\n" "${dbname}" "${bname}" "${line}" "${msg}"
}

function printf_with_location()
{
    param_count_check 1 "$#"  printf-with-location
    _printf_with_location_ 1 "${1}"
}

function printf_info() {
    param_count_check "1" "$#" printf-info
    _printf_with_location_ 1 "INFO: ${1}"
}
# Set this to control the debug output
if [ x"${BASH_HELPERS_DEBUG_LEVEL}" == x"" ]
then
       export BASH_HELPERS_DEBUG_LEVEL=0
fi

function verbose_printf() {
    param_count_check "2" "$#" verbose-printf
    local level
    local msg
    level="$1"
    msg="$2"

    if [ "${level}" -le "${BASH_HELPERS_DEBUG_LEVEL}" ]
    then
	_printf_with_location_ 1 "DBG: ${msg}"
    fi
}

function fatal_error() {
    # We do not check parameter count here
    local msg="${@}"
    printf "*** FATAL *** FATAL *** FATAL *** FATAL *** FATAL *** FATAL ***\n"
    dump_bash_callstack
    printf_with_location "FATAL: ${msg}"
    printf "*** FATAL *** FATAL *** FATAL *** FATAL *** FATAL *** FATAL ***\n"
    exit 1
}
