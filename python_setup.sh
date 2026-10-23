#! /bin/bash

if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    printf "PROJ_ROOT_DIR is not defined it is requred\n"
    exit 1
fi

# Look for our python Virtual Env Directory.
expected="${PROJ_ROOT_DIR}/.venv"
if [ x"${PROJ_VENV_DIR}" == x"" ]
then
    export PROJ_VENV_DIR="${expected}"
else
    if [ "${PROJ_VENV_DIR}" != "${expected}" ]
    then
	printf "PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
	printf "PROJ_VENV_DIR=%s\n" "${PROJ_VENV_DIR}"
	printf "     expected=$\n" "${expected}"
	printf "Not consistent, please fix\n"
	exit 1
    fi
fi

tmp="${PROJ_PYTHON_DIR}/create_venv.py"
if [ ! -d "${PROJ_VENV_DIR}" ]
then
    # If the VENV does not exist - go create it.
    ${PROJ_PYTHON3_EXE} "${PROJ_PYTHON_DIR}/create_venv.py"
fi

${PROJ_PYTHON3_EXE} "${PROJ_PYTHON_DIR}/update_venv.py"

# Now, Activate the that VENV.
# If we are on WINDOWS:
if [ x"${APPDATA}" == x"" ]
then
    # Linux/Mac
    source "${PROJ_VENV_DIR}/bin/activate"
else
    # Windows
    source "${PROJ_VENV_DIR}/Scripts/activate"
fi

expected="${PROJ_ROOT_DIR}/.vscode"
if [ x"${PROJ_VSCODE_DIR}" == x"" ]
then
    export PROJ_VSCODE_DIR="${expected}"
else
    if [ "${PROJ_VSCODE_DIR}" != "${expected}" ]
    then
	printf "  PROJ_ROOT_DIR=%s\n" "${PROJ_ROOT_DIR}"
	printf "PROJ_VSCODE_DIR=%s\n" "${PROJ_VSCODE_DIR}"
	printf "       expected=$\n" "${tmp}"
	printf "Not consistent, please fix\n"
	exit 1
    fi
fi

${PROJ_PYTHON3_EXE} "${PROJ_PYTHON_DIR}/update_vscode.py"

tmp="${PROJ_ROOT_DIR}/.idea"
# We do not export this.
${PROJ_PYTHON3_EXE} "${PROJ_PYTHON_DIR}/update_pycharm.py"

