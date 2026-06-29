# This is all about how this PROJECT sets up and uses Python.

## Commentary:

At this point in Pythons life it has reached the old "DLL HELL"
problem that early Microsoft Windows users had/have.

By that I mean - each thing has its own version of python
and that version of Python has its own crap it comes with.

And they are all incompatible with each other.

Example:  Xilinx provides its own private version of Python.

Example:  Microsoft provides a version of Python in Excell.

Example:  You may have installed Python for your purposes

Do you think all of these are compatible with each other?
Yea, partly they are, and partly they are not.

But this is solved by "Virtual Environments" yea sort of.  Each of
those damn tools say NO you shall use our virtual environment.

## Sadly - we do the same..

To help with this, we do the following:

We make use of this Environment Variable.

   [For details see docs/development_environment.md](docs/development_environment.md)

```bash
   export PROJ_PYTHON3_EXE=/path/to/your/python.exe

   # Most often this is just export PROJ_PYTHON3_EXE=`which python3`
   # But sometimes it needs to be a different python.
```

## We do create a virtual environment (VENV)

   By default, we place this in the directory LOSTARM_VENV_DIR Which is
   normally located, here the default value is:

   	    LOSTARM__VENV_DIR=${PROJ_ROOT_DIR}/.venv

   And we do install packages into the VENV.

## When the VENV is created, we create two bat/shell scripts.

   
   