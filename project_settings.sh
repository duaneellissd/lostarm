#! /bin/bash
# The intent is you "source" this file ONCE

calling_script=`realpath ${BASH_SOURCE[0]}`
calling_dir=`dirname ${calling_script}`
source ${calling_dir}/helper-scripts/bash/bash_helpers.sh

# Double inclusion check.
if [ x"${GUARD_PROJECT_SETTINGS_SH}" == x"" ]
then
    export GUARD_PROJECT_SETTINGS_SH=`realpath ${BASH_SOURCE[0]}`
fi

expected=

#========================================
# detect DOUBLE sourcing/inclusion of this file.
# AND - the wrong file being sourced
#========================================
# absolute path to this file
tmp=`realpath ${BASH_SOURCE[0]}`
# Now check our INCLUDE GUARD
if [ x"${tmp}" == x"${LOSTARM_GUARD_PROJECT_SETTINGS_SH}" ]
then
    # Double inclusion - leave
    if $LOST_ARM_VERBOSE
    then
	printf "%s: Avoid double inclusion\n" "${tmp}"
    fi
    return
fi
# Set the include guard.
if [ x"${LOSTARM_GUARD_PROJECT_SETTINGS_SH}" == x"" ]
then
    export LOSTARM_GUARD_PROJECT_SETTINGS_SH="${tmp}"
fi

# We have been included, make sure we are in the same project.
if [ "${tmp}" != "${LOSTARM_GUARD_PROJECT_SETTINGS_SH}" ]
then
    # this happens when somebody has 2 copies of the project.
    # They go into the first copy/directory(A) and
    #   Next they source copy(A)project_settings.sh
    #   The env vars are now setup for directory(A)
    # LATER...
    #   They enter copy/directory(B) [the other copy]
    #   And they source copy(B) project settings.
    #
    # The BAD RESULT:
    #   The variables are mixed up and point to the wrong place.
    #   That needs to be stopped right now otherwise bad things occur.
    printf "Mis-matched PROJECT_SETTINGS:\n"
    printf "new: %s\n" "${tmp}"
    printf "old: %s\n" "${LOSTARM_GUARD_PROJECT_SETTINGS_SH}"
    exit 1
fi
# Declare the PROJ_ROOT_DIR - everything is based on this.
export PROJ_ROOT_DIR=${tmp}
# Our HELPER scripts are located here.
export HELPER_SCRIPTS_DIR=${PROJ_ROOT_DIR}/helper-scripts
# The BASH Helpers are here.
tmp="$HELPER_SCRIPTS_DIR/bash/bash_common.sh"
if [ ! -f "$tmp" ]
then
    echo "Missing: $tmp"
    exit 1
fi
source "$tmp"

# Now, set up other variables via the helper functions.
provide_default PROJ_ROOT_DIR      "$PROJ_ROOT_DIR"
provide_default HELPER_SCRIPTS_DIR "$HELPER_SCRIPTS_DIR"
provide_default BASH_HELPER_DIR    "$HELPER_SCRIPTS_DIR/bash"
provide_default PYTHON_HELPER_DIR  "$HELPER_SCRIPTS_DIR/python"

# Now fetch the PYTHON settings for the project.
tmp=${PROJ_ROOT_DIR}/python_settings.sh
echo "Source: ${tmp}"
source "$tmp"

echo "END: ${BASH_SOURCE[0]}"
