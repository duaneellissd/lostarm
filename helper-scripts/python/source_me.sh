#! /bin/bash

tmp=`realpath "${BASH_SOURCE[0]}"`
expected=`dirname "${tmp}"`

if [ x"${PROJ_PYTHON_DIR}" != x"${expected}" ]
then
    printf "  PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
    printf "PROJ_PYTHON_DIR=%s\n" "${PROJ_PYTHON_DIR}"
    printf "       expected=%s\n" "${expected}"
    printf "this is not consistent"
    exit 1
fi

# We require a defintion of PROJ_PYTHON3_EXE.
if [ x"${PROJ_PYTHON3_EXE}" == x"" ]
then
    printf "PROJ_PYTHON3_EXE is not defined, it is required\n"
    exit 1
fi

# And it must be an executable.
if [ ! -x "${PROJ_PYTHON3_EXE}" ]
then
    printf "${PROJ_PYTHON3_EXE} not executable\n"
    exit 1
fi

# We need THIS added to the PYTHON PATH.
tmp="${PROJ_PYTHON_DIR}/modules"

# BUT first - if it is already in the path..
if [[ ":${PYTHONPATH}:" == *":${tmp}":* ]]; then
    # Do not add it to the path a second time.
    echo "already in the path" >> /dev/null
else
    # Ok -not in the path...

    # Is the path EMPTY?
    if [ x"${PYTHONPATH}" == x"" ]
    then
	# empty.. non existent just use ours.
	PYTHONPATH="${tmp}"
    else
	# Not empty, put ours at the front.
	PYTHONPATH="${tmp}":"${PYTHONPATH}"
    fi
fi
# Export this for the world to find.
export PYTHONPATH

# If the VENV does not exist... create it.
if [ ! -d ${PROJ_VENV_DIR} ]
then
    # create the VENV.
    ${PROJ_PYTHON3_EXE} "${PROJ_PYTHON_DIR}/create_venv.py"
fi
