#! /bin/bash
# The intent is you "source" this file

VERBOSE=0
if [ "$1" == "-v" ]
then
    shift
    let VERBOSE="$VERBOSE"+1
fi
export VERBOSE
    

tmp=`realpath ${BASH_SOURCE[0]}`

if [ "$PROJECT_SETTINGS_SH" != "" ]
then
    # did somebod source one 'project-settings'
    if [ "$PROJECT_SETTINGS_SH" == "$tmp" ]
    then
	# Thats ok if the filenames are the same
	printf "already sourced: $PROJECT_SETTINGS_SH"
	return
    else
	# then try to source a different one?"
	printf "PROJECT_SETTINGS_SH=%s\n" "$PROJECT_SETTINGS_SH"
	printf "But does not match: %s\n" "$tmp"
	exit 1
    fi
fi

export PROJECT_SETTINGS_SH="$tmp"
tmp=`dirname "${PROJECT_SETTINGS_SH}"`
if [ "$PROJ_ROOT_DIR" != "" ]
then
    if [ "$PROJ_ROOT_DIR" == "$tmp" ]
    then
	# same all is well ignore this.
	echo "ignored" >> /dev/null
    else
	# two different PROJ_ROOT_DIRS is not allowed
	printf "      PROJ_ROOT_DIR=%s\n" "$PROJ_ROOT_DIR"
	printf "But does not match: %s\n" "$tmp"

	exit 1
    fi
fi

export PROJ_ROOT_DIR=${tmp}

export HELPER_SCRIPTS_DIR=${PROJ_ROOT_DIR}/helper-scripts

# Get our common things.
source ${HELPER_SCRIPTS_DIR}/bash/bash-common.sh
show_var PROJ_ROOT_DIR
show_var HELPER_SCRIPTS_DIR

source ${PROJ_ROOT_DIR}/python_settings.sh

