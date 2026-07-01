#! /bin/bash

# Die on simple errors.
set -e
#========================================
# This is a set of functions to simplify
# Writing bash scripts.
#----------------------------------------
# We attempt to follow this standard:
#  Widely used, Exported things are SNAKE_CASE_CAPS
#  Private things are snake_lower_strings.
#========================================

tmp=$(realpath ${BASH_SOURCE[0]})
tmp=$(dirname "$tmp")

# Bash type "include guard"
if [ "${BASH_HELPERS_SH}" = "" ]
then
    export BASH_HELPERS_SH="$tmp"
else
    if [ "$tmp" == "${BASH_HELPERS_SH}" ]
    then
        echo "BashHelper already included"
        return
    else
        printf "This seems wrong?\n"
        printf " THIS FILE: %s\n" "$tmp"
        printf "OTHER FILE: %s\n" "${BASH_HELPERS_SH}"
        exit 1
    fi
fi
export BASH_HELPERS_SH="$tmp"

# shellcheck disable=SC2317
function caller_show()
{
  local depth
  local lineno
  local func_name
  local filename
  depth="$1"
  msg="$2"
  #caller 1
  #caller 2
  #caller 3
  lineno=$(caller "$depth" | cut -d' ' -f 1)
  func_name=$(caller "$depth" | cut -d' ' -f 2)
  filename=$(caller "$depth" | cut -d' ' -f 3)
  if [ "$VERBOSE" -lt 1 ]
  then
     filename=`basename "$filename"`
  fi
     

  #echo "LN=${lineno} FUNC=${func_name} FN=${filename}"

  # shellcheck disable=SC2317
  printf "%s:%d: %s: %s\n" "${filename}" "${lineno}" "${func_name}" "${msg}"
}

function caller_fatal()
{
    caller_show "$1" "FATAL: $2"
    exit 1
}

function caller_info()
{
    caller_show "$1" "INFO: $2"
}

# shellcheck disable=SC2317
function must_be_defined()
{
    local variable_name
    variable_name="$1"
    local value
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

# shellcheck disable=SC2317
function provide_default()
{
    local variable_name
    variable_name="$1"
    local value
    value="$2"
    local old_value
    old_value="${!variable_name}"
    if [ "${old_value}" == "" ]
    then
      declare "${variable_name}=${value}"
      caller_show 1 "provide_default ${variable_name}=${value}"
    else
      old_value="${value}"
      caller_show 1 "already-set ${variable_name}=${old_value}"
    fi
    # shellcheck disable=SC2163
    echo "AA"
    export "${variable_name}"="${value}"
    echo "BB"
}

function show_var()
{
    NAME="$1"
    VALUE="${!NAME}"

    caller_show 1 "${NAME}=${VALUE}"
    export "${NAME}"
}

show_var BASH_HELPERS_SH
