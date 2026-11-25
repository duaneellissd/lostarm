#! /bin/bash
#========================================
# This sets up our python environment.

THIS_FILE=`realpath ${BASH_SOURCE[0]}`

#--------------------------------------------------
# STEP 1: Belt and suspenders - Verify we are using BASH.
#--------------------------------------------------

if [ x"${BASH_VERSION}" == x"" ]
then
    echo "This does not appear to be BASH"
    echo "BASH is required by this and other scripts"
    exit 1
fi

#--------------------------------------------------
# STEP 2: Belt and suspenders - Verify PROJ_ROOT_DIR is set.
#--------------------------------------------------

if [ x"${PROJ_ROOT_DIR}" == x"" ]
then
    echo "The variable PROJ_ROOT_DIR is missing it is required"
    echo "It should have been set by \${PROJ_ROOT_DIR}/source_me.sh"
    exit 1
fi

#----------------------------------------
# STEP 3: the rest of this is hard in bash
#         and easier to do in python, so we switch.
#----------------------------------------
if [ x"${PROJ_PYTHON_EXE}" == x"" ]
then
    echo "PROJ_PYTHON_EXE is not set, it is required"
    exit 1
fi

${PROJ_PYTHON_EXE} ./python_setup.py
if [ $? -ne 0 ]
then
    echo "PYTHON Setup has failed"
    exit 1
fi
echo "PYTHON setup has succeeded"
echo "Please activate your python env as follows:\n"
echo "."

function show_unix_methods() {
    name="$1"
    echo "On $name:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    source .venv\bin\activate     <-- This is ALWAYS required"
    echo "."
    echo "    To launch VsCode, type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    bash ./run_code.sh"
    echo "."
    echo "    To launch PyCharm (if it is installed), type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    bash ./run_pycharm.sh"
    echo "."
}

function show_cmd_exe_methods() {
    echo "Using CMD.EXE (not power shell)"
    echo "."
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    .venv\Scripts\activate.bat    <-- This is ALWAYS required"
    echo "."
    echo "    To launch VsCode, type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    run_code.bat"
    echo "."
    echo "    To launch PyCharm (if it is installed), type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    run_pycharm.bat"
    echo "."
}

function show_powershell_methods() {
    echo "On Windows, Using PowerShell V5 (ships with windows 11)"
    echo "Using a newer version of powershell - you are on your own"
    echo "."
    echo ". At the powershell prompt, type: $PSVersionTable.PSVersion"
    echo ". Version 5.1 - works great, others not so much :-("
    echo "."
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    .venv\Scripts\activate.ps1    <-- This is ALWAYS required"
    echo "."
    echo "    To launch VsCode, type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    run_code.ps1"
    echo "."
    echo "    To launch PyCharm (if it is installed), type:"
    echo "    cd \${PROJ_ROOT_DIR}"
    echo "    run_pycharm.ps1"
    echo "."
}

case "$OSTYPE" in
    "linux"*|"darwin"*|"freebsd"*|"solaris"*)
        show_unix_methods("UNIX Like Platforms")
        ;;
    "cygwin"*|"msys"*)
        show_unix_methods("Using GITBASH on windows is not that great")
        show_cmd_exe_methods()
        show_powershell_methods()
        ;;
    *)
        echo "Unknown OSTYPE=${OSTYPE}"
        exit 1
        ;;
esac
exit 0
