#! /bin/bash

tmp=`dirname "${BASH_SOURCE[0]}"`
source "${tmp}/printf_helpers.sh"


function show_variable()
{
    param_count_check "1" "$#" "showvars:args=${@}"

    local call_depth
    local var_name
    local value

    call_depth=1
    var_name="${1}"
    # fetch the value.
    value="${!var_name}"
    # print the value
    _printf_with_location_ "${call_depth}" $(printf "%s=%s" "${var_name}" "${value}")
}

function required_variable( )
{
    # DIE if the variable is not defined.
    local var_name="${1}"
    local value

    # get the value of the variable as it is now.
    value="${!var_name}"

    # if the variable is not defined
    if [ x"${value}" == x"" ]
    then
	# then it is a fatal error
	fatal_error $(printf "Var: %s is not defined" "${var_name}")
    fi
    # Inform user of the value
}

function default_variable()
{
    # if the variable is not defined then provide a default value
    param_count_check "2" "$#" default-vars

    local var_name
    local default_value
    local tmp

    var_name="${1}"
    default_value="${2}"

    tmp="${!var_name}"

    # test if the variable is defined.
    if [ x"${tmp}" == x"" ]
    then
	# it is not, so provide a value
	export "${var_name}=${default_value}"
	# Set tmp for below
	tmp="${default_value}"
    fi
    # Inform the user of the value
    printf_info $(printf "%s=%s" "${var_name}" "${tmp}")
}

function check_variable()
{
    param_count_check "2" "$#" check-variable
    local var_name
    local expected_value
    local tmp

    var_name="${1}"
    expected_value="${2}"

    tmp="${!var_name}"

    read -r line func file <<< `caller 1`
    if [ x"${tmp}" == x"${expected_value}" ]
    then
        printf "%s:%d: Variable: %s expected to be: %s\n" "$file" "$line" "$var_name" "$expected_value"
        printf "Actual value: %s" "${tmp}"
        exit 1
    fi
    printf_info $(printf "%s=%s" "${var_name}" "${tmp}")
}
