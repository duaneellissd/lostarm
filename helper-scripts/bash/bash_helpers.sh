#! /bin/bash
#========================================
# NOTE: seemingly excessive quoting in this file
# REASON:  Future WindBlows paths with whitespace in paths.
#========================================

# Die on simple errors.
set -e

this_file=`realpath ${BASH_SOURCE[0]}`
this_dir=`dirname ${this_file}`
# are we being included multiple times?
case "${GUARD_BASH_HELPERS_SH}" in
    "${this_file}")
	# We have been included already.
	# and our name matches so we are good.
	# 'return' exits the 'sourced script'
	return
	;;
    "")
	# This is the first time we are included.
	# set our guard variable to detect future includes
	export GUARD_BASH_HELPERS_SH="${this_file}"
	;;
    *)
	#========================================
	# This happens when: you have 2 copies of the package
	# A) Copy A is in directory A and you have sourced things.
	# B) Copy B is in directory B and you are sourcing again.
	# THUS .. half the variables point at (A)
	# And the other half point at (B)
	# Things are going to go bad so we stop this
	#========================================
	
	printf "Invalid Directory construct\n"
	printf "EXPECTED: %s\n" "${GUARD_BASH_HELPERS_SH}"
	printf "  ACUTAL: %s\n" "${this_file}"
	exit 1
	;;
esac
    

# Somebody sourced us, did they call us correctly?
if [ ! -d "${calling_dir}" ]
then
    printf "ERROR: calling_dir=%s is not a directory\n" "${calling_dir}"
    exit 1
fi

if [ ! -f "${calling_script}" ]
then
    printf "ERROR: calling_script=%s is not a file\n" "${calling_script}"
    exit 1
fi

case "${LOSTARM_VERBOSE}" in
    "true" | "false")
	# all is well.
	;;
    "")
	# not set, provide a default.
	export LOSTARM_VERBOSE=false
	;;
    *)
	# set to something wacky.
	printf "LOSTARM_VERBOSE=%s\n" "${LOSTARM_VERBOSE}"
	printf "This must be exactly: 'true' or 'false'\n"
	exit 1
	;;
esac


#========================================
# This is a set of functions to simplify
# Writing bash scripts.
#----------------------------------------
# We attempt to follow this standard:
#  Widely used, Exported things are SNAKE_CASE_CAPS
#  Private things are snake_lower_strings, not KABOB-CASE
#=================================

# shellcheck disable=SC2317
function caller_show()
{
    # This is a core debug function used by multiple things.
    local depth
    local lineno
    local func_name
    local filename
    # DEPTH tells us how far up the call stack to grab the filename/lineno.
    depth="$1"
    # our message to print is parameter 2.
    msg="$2"
    #caller 1
    #caller 2
    #caller 3
    lineno=$(caller "$depth" | cut -d' ' -f 1)
    func_name=$(caller "$depth" | cut -d' ' -f 2)
    filename=$(caller "$depth" | cut -d' ' -f 3)
    if "$LOSTARM_VERBOSE"
    then
	echo "Nothing to do" >> /dev/null
    else
	# use just the basename 
	filename=`basename "$filename"`
    fi
    # shellcheck disable=SC2317
    # this error format is important.
    # Many tools recognize this format and will make it clickable
    printf "%s:%d: %s: %s\n" "${filename}" "${lineno}" "${func_name}" "${msg}"
}
# make this visible
export -f caller_show

function caller_fatal()
{
    # The caller has decided we shall die in a fatal way.
    caller_show "$1" "FATAL: $2"
    exit 1
}
export -f caller_fatal

function caller_info()
{
    # The caller just wants to print a informational message.
    caller_show "$1" "INFO: $2"
}
export -f caller_info


# shellcheck disable=SC2317
function must_be_defined()
{
    # The VARIALBE name must be defined otherwise it is an error.
    local variable_name
    variable_name="$1"
    local value
    # Fetch the value.
    value="${!variable_name}"
    if [ "${value}" == "" ]
    then
        msg=$(printf "Variable: %s is not defined it is required\n" "${variable_name}")
        caller_fatal 2 "$msg"
    else
        msg=$(printf "Variable: %s=%s" "${variable_name}" "${value}")
        caller_info 2 "$msg"
    fi
}
export -f must_be_defined

# shellcheck disable=SC2317
function provide_default()
{
    # If the variable is not yet defined, then use $2 as the default
    local variable_name
    variable_name="$1"
    local value
    value="$2"
    local old_value
    old_value="${!variable_name}"
    if [ "${old_value}" == "" ]
    then
	eval ${variable_name}=${value}
	caller_show 1 "provide_default ${variable_name}=${value}"
    else
	old_value="${value}"
	caller_show 1 "already-set ${variable_name}=${old_value}"
    fi
    # shellcheck disable=SC2163
    export ${variable_name}
}
export -f provide_default

function show_var()
{
    # The caller wants to print/show the specified variable.
    NAME="$1"
    # Fetch the value.
    VALUE="${!NAME}"

    caller_show 1 "${NAME}=${VALUE}"
    export "${NAME}"
}
export -f show_var


