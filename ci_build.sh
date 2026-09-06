#! /bin/bash
#========================================
# Tell BASH to die if there is an error.
set -e

#========================================
# The intent is the CI (automated build) executes this script.
# NOTHING is set, no variables are setup etc.
# This exists so we have an easy way to build in a ci/cd system.
# AND - we can easily replicate the ci/cd build locally.
#========================================
# The intent is this script lives at the root(TOP DIR) of the project.

# step 1 - the abs path to this script.
calling_script=`realpath ${BASH_SOURCE[0]}`
# step 2 - the directory name of this project.
PROJ_ROOT_DIR=`dirname ${calling_script}`
# make this visible to everything.
export PROJ_ROOT_DIR

# The CI Build script takes options to decide what to build.
function usage()
{
    printf "Usage: %s [-h] [-v] [-c CROSS] FILENAME_TARGETLIST\n"
    exit 1
}

fn_TARGET_LIST=""
CROSS_LIST=""

shopt -s extglob
while [[ "$#" -gt 0 ]]
do
    case "$1" in
       '-h' | '--help' | '-?' )
	    usage
	    ;;
       '-v' | '--verbose')
	   export LOSTARM_VERBOSE=true
	   shift
	   ;;
       '-c' | '--cross')
	   # shift, go past the -c or --cross
	   tmp="${1}"
	   if [ x"${tmp}" == x"" ]
	   then
	       printf "Invalid --cross option: %s\n" "${tmp}"
	       usage
	       exit 1
	   fi
	   CROSS_LIST="${CROSS_LIST} ${tmp}"
	   shift
	   continue
	   ;;
       
       ([a-zA-Z0-9_\.])
	   if [ x"${fn_TARGET_LIST}" == "" ]
	   then
	       fn_TARGET_LIST="${1}"
	       shift
	       continue
	   else
	       usage
	       exit 1
	   fi
	   ;;
       *)
	   usage
	   exit 1
	   ;;
    esac
done

# get all of our settings.
source ${PROJ_ROOT_DIR}/all_settings.sh

# If we where not given a project list filename
# then choose a default one.

if [ "${fn_TARGET_LIST}" == x"" ]
then
    fn_TARGET_LIST="all_targets/cicd_default.txt"
else
    fn_TARGET_LIST="${new_fn_TARGET_LIST}"
fi

# A target is a directory where a project lives.
# a fn_TARGET_LIST is a file listing a bunch of projects.
# 
if [ ! -f "${fn_TARGET_LIST}" ]
then
    printf "%s: No such file or directory\n" "${fn_TARGET_LIST}"
    exit 1
fi

TARGET_LIST=`grep -v '^#' ${fn_TARGET_LIST}`
# what is the name of this file?
set -x

set | grep PROJ
source ${PROJ_ROOT_DIR}/all_settings.sh



