#! /bin/bash
#============================================================
# PURPOSE OF THIS SCRIPT.
#
#   This overall system uses a number of shell variables
#   This script either:
#        (A) sets those variables
#   or   (B) verifies and exits/dies if they are not set.
#   and  (C) Sets a number of other variables.
#
#   More detail can be found in:
#        ${PROJ_HELPER_DIR}/docs.
#============================================================
#
if [ "x${BASH_VERSION}" == x"" ]
then
    printf "This does not appear to be BASH.\n"
    printf "These scripts require BASH\n"
    exit 1
fi

# scripts should DIE/exit-non-zero on any simple error.
set -e

# Where is this file Located?
tmp=`realpath "${BASH_SOURCE[0]}"`
dtmp=`dirname "${tmp}"`
#==================================================
# Here we determine the location of PROJ_ROOT_DIR
#==================================================
#
# This file is at the ROOT so we can calculate the value.
if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    # Not set - then set it.
    export PROJ_ROOT_DIR="${dtmp}"
fi

#----------------------------------------
# SANITY CHECK.
# Consider the following:
#    You are bouncing between two directories A and B.
#    You have sourced/setup for Directory A.
#    You goto directory B and "setup again"
#    BUT things are still set for A...
#    The variables are now "mixed and confused" things go wrong.
#
#    We want to stop that wrong ness.
#----------------------------------------
# Note:"dtmp" was set above.
if [ "${PROJ_ROOT_DIR}" != "${dtmp}" ]
then
    printf "PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
    printf "     expected=%s\n" "${dtmp}"
    printf "not consistent, please fix\n"
    exit 1
fi
# Make this visible to all other children of our self.
export PROJ_ROOT_DIR

#--------------------------------------------------
# We will create our own Python Virtual Environment.
export PROJ_VENV_DIR=${PROJ_ROOT_DIR}/.venv

#----------------------------------------
# I use VSCODE, as do many others.
# lower level scripts will create/populate this with helpful settings.
# BUT - that lower level script needs to know where ".vscode" lives.
# This provides that location to the lower level scripts.
export PROJ_VSCODE_DIR=${PROJ_ROOT_DIR}/.vscode

#----------------------------------------
# To de-clutter the root directory
# We move many "helper like things" into the
# GIT SUB MODULE: 'proj-helper-scripts'
# By making this a GIT_SUBMODULE other projects
# can reuse the 'proj-helper-scripts'.
#----------------------------------------
# NOTE: there is a large list of python modules there too.
# see: ${PROJ_HELPER_DIR}/python/modules
#----------------------------------------
# We expect to find our helpers here.
tmp="${PROJ_ROOT_DIR}/proj-helpers"
# If this is not set, then set it.
if [ x"${PROJ_HELPER_DIR}" == x"" ]
then
    export PROJ_HELPER_DIR="${tmp}"
fi

echo "PROJ_HELPER_DIR: ${PROJ_HELPER_DIR}"

if [ "${PROJ_HELPER_DIR}" != "${tmp}" ]
then
    echo "THIS_FILE: ${THIS_FILE}"
    echo "expected: PROJ_HELPER_DIR=${tmp}"
    echo "  actual: PROJ_HELPER_DIR=${PROJ_HELPER_DIR}"
    exit 1
fi

# source things and set additional ENV vars.
source ${PROJ_HELPER_DIR}/source_me.sh

# Now, execute (donot source) our python setup script
bash "${PROJ_ROOT_DIR}/python_setup.sh"
