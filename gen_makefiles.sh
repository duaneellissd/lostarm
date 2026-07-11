#! /bin/bash

if [ "$LOSTARM_VENV_DIR" == "" ]
then
	echo "Missing LOSTARM_VENV_DIR"
	exit 1
fi 

if [[ ":${PATH}:" == *":${LOSTARM_VENV_DIR}/bin:"* ]]
then
    echo LOSTARM_VENV_DIR is in the path
else
    echo "The LOSTARM_VENV_DIR is not activated."
    echo "This is required"
    exit 1
fi
    
$LOSTARM_PYTHON3_EXE gen_makefiles.py
