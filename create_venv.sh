
#! /bin/bash

tmp=`realpath ${BASH_SOURCE[0]}`
tmp=`dirname $tmp`
if [ "$PROJ_ROOT_DIR" == "" ]
then
    source ${tmp}/project_settings.sh
fi

source ${PROJ_ROOT_DIR}/helper-scripts/bash/bash-common.sh


