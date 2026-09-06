# This is all about how this PROJECT sets up and uses Python.

## To define some variables

Please see: ${GIT_ROOT_DIR}/ENV_VARS.md

PROJ_ROOT_DIR - see ${GIT_ROOT_DIR}/README.md

LOSTARM_P
LOSTARM_PYTHON_DIR - normally: ${PROJ_ROOT_DIR}/
LOSTARM_PYTHON_VENV_DIR - normally: ${PROJ_ROOT_DIR}/.venv
    s where we create our python Venv.
       this is normally ${PROJ_ROOT_DIR}/.venv
    LOSTARM_PYTHON_HELPER_DIR - is where we have more python things.
    
    ```

## Commentary Why does this exist?

At this point in Pythons life it has reached the old "DLL HELL"
problem that early Microsoft Windows users had/have.

By that I mean - each thing has its own version of python
and that version of Python has its own crap it comes with.

And they are all incompatible with each other.

Example: I do most of my development on my x86 MACBOOK
	 How many versions of Python do I have?
	 /Library/Python/2.7
	 /Library/Python/3.7
	 /Library/Python/3.9
	 /Applications/ti/ccs2002/.../python3

Example: On Linux
	 There is the system version of Python.
	 My Xilinx tools have their private version of Python.
	 My Microchip/MicroSemi has its private version of Python.

Example: On Windows:
	 i have the 'company approved version'
	 I have the one that came from Xilinx
	 And the one from Microchip/MicroSemi.
	 And the one built into Microsoft Excell.

In many cases, these other tools have/need/require a binary interface
to python, and that is a problem.  The biggest example is GDB comes
with Python plugins now for over 10 years.

BUT which binary version of Python was used for that feature? And for
my other tasks & needs that other host tool is required and that requires
that tools private version of Python. Grrr!

Why can't these vendors use the default version of Python?  Or some
other version of python? For a software IDE it is important that it
works.  And to get GDB_PY to work, you require the matching Python
Binary it was compiled and linked against.

To solve that vendors include their private copy of python.  And each
of those vendors are on a seperate release schedule and cadence.  That
is a problem and makes it really hard.

## BUT that is what a PYTHON VENV was designed for..

Yea, please explain to these vendors that their launch scripts
shall *NOT* override various PYTHON variables.

## Oh and how does your Python IDE find which version of python to use?

## And where does the IDE's Language Server find these modules?

VSCODE uses the ${PROJ_ROOT_DIR}/.vscode directory.

PYCHARM uses an environment variable called PYTHONPATH Damn them they
should use PYCHARM_PYTHON_PATH or something unique to them but they do not.

## My solution is in several parts.

### PART 1:

    DO NOT Ever use the PATH version of PYTHON.
    in stead, we require a UNIQUE variable LOSTARM_PYTHON_EXE
    This must exist and point to the version of python to use.
    If it does not exist, we die with a nasty error.

    We could continue on and let it die later when something goes wrong.
    No - done enough customer/developer support to not want to do more.
    so if it does not seem correct, we die with a non-zero exit.

### PART 2:

    Yes, we do create our own PYTHON Virtual Environment.
    Grep various files for "LOSTARM_PYTHON_VENV_DIR" for details.

### PART 3:

    Where possible Avoid Python Modules, Avoid PIP
    Really there are only a few really useful ones.

### Part 4:

    For my DAY $JOB$ I work in a very high security place.
    I have zero internet access, and I cannot bring thumb drives in.

    Solution: include copies of all python modules in the project.
    Generally they are small and simple. I will simply reject things
    that are not small and simple add ons.

    These are stored in ${LOSTARM_PYTHON_HELPER_DIR}/modules/pip-modules
    

### Part 5:

    I also work on multiple machines, Mac, Windows, Linux.  Many
    python modules come as "wheel" (WHL) files. Which are universal.

    BUT - sometimes you require the binaries, ie: 'cryptography'

###
    So - where possible I include
    all PYTHON Modules in the python helper directory.
    I prefer the WHL files as they are universal across all platforms.
    
    HOWEVER some things are binary, ie: Python crypto library.

    So in the ${PY
    Always prefer the Python standard Library for everything.
   Sadly, Modules & Pip are too much to ask.


   
   Where possible write all python to use only the python standard lib.
   There are a few execptions

Do you think all of these are compatible with each other?
Yea, partly they are, and partly they are not.

But this is solved by "Virtual Environments" yea sort of.  Each of
those damn tools say NO you shall use our virtual environment.

## Sadly - we do the same..

To help with this, we do the following:

We make use of this Environment Variable.

   [For details see docs/development_environment.md](docs/development_environment.md)

```bash
   export LOSTARM_PYTHON3_EXE=/path/to/your/python.exe

   # Most often this is just export LOSTARM_PYTHON3_EXE=`which python3`
   # But sometimes it needs to be a different python.
```

## We do create a virtual environment (VENV)

   By default, we place this in the directory LOSTARM_VENV_DIR Which is
   normally located, here the default value is:

   	    LOSTARM__VENV_DIR=${PROJ_ROOT_DIR}/.venv

   And we do install packages into the VENV.

## When the VENV is created, we create two bat/shell scripts.

   
   