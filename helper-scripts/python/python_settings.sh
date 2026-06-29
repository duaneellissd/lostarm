#! /bin/bash

if [ "$LOSTARM_PYTHON_EXE" == "" ]
then
	echo "LOSTARM_PYTHON_EXE is not defined it is required"
	exit 1
fi

if [ "$LOSTARM_VENV_DIR" == "" ]
then
	echo "LOSTARM_VENV_DIR is not defined it is required"
	exit 1
fi

