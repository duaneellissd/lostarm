#! /bin/bash

if [ "$PROJ_VENV_DIR" == "" ]
then
	echo "Missing PROJ_VENV_DIR"
	exit 1
fi 

if [[ ":${PATH}:" == *":${PROJ_VENV_DIR}/bin:"* ]]
then
    echo PROJ_VENV_DIR is in the path
else
    echo "The PROJ_VENV_DIR is not activated."
    echo "This is required"
    exit 1
fi
    
$PROJ_PYTHON3_EXE gen_makefiles.py
