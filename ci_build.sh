#! /bin/bash
#========================================
# Tell BASH to die if there is an error.
set -e

#========================================
# The intent is the CI (automated build) executes this script.
# NOTHING is set, no variables are setup etc.
# NO Parameters are passed (ok, there are a very few below)
#----------------------------------------
# If you are running this on YOUR ci/cd system.
# You may need to 'hard code' the python location.
# in a way specific to your CI/CD system you use.

#========================================
# This script should be found at: ${PROJ_ROOT_DIR}/ci_build.sh

# You may need to change this to fit your systems needs.
PROJ_PYTHON_EXE=/usr/local/bin/python3
# for more info, see: ${PROJ_HELPER_DIR}/docs/ALL_ABOUT_PYTHON.m

source ./source_me.sh

# Use Python to simplify this.
${PROJ_PYTHON_EXE} ${PROJ_PYTHON_DIR}/ci_build.py "$@"




