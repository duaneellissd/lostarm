#! /bin/bash
#========================================
# Tell BASH to die if there is an error.
set -e

#========================================
# The intent is the CI (automated build) executes this script.
# NOTHING is set, no variables are setup etc.
# NO Parameters are passed (ok, there are a very few below)
#========================================
# This exists so we have an easy way to build in a ci/cd system.
# AND - we can easily replicate the ci/cd build locally.
#========================================
# The intent is this script lives at the root(TOP DIR) of the project.

# step 1 - the abs path to this script.
THIS_FILE=`realpath ${BASH_SOURCE[0]}`
# step 2 - the directory name of this project.
PROJ_ROOT_DIR=`dirname ${THIS_FILE}`
# make this visible to everything.
export PROJ_ROOT_DIR


# We need Python, we'll take the default
# BUT sometimes you need to specify your own.
PROJ_PYTHON3_EXE=`which python3`
if [ ! -x ${PROJ_PYTHON3_EXE} ]
then
    PROJ_PYTHON3_EXE=`which python`
fi
if [ ! -x ${PROJ_PYTHON3_EXE} ]
then
    printf "Cannot find python, please set PROJ_PYHON3_EXE and try again\n"
    exit 1
fi
  

source ${PROJ_ROOT_DIR}/all_settings.sh

# Use Python to simplify this.
${PROJ_PYTHON3_EXE} ${PROJ_ROO_DIR}/ci_build.py "$@"




