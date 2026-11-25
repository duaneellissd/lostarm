# These are the ENV Vars, and a road map to many things.

## What sets the vars?

Option 1 - You can preset a number of them and that is acceptable (to some degree)

Option 2 - They are set by the "source_me.sh" script in that directory.

Generally, any source_me.sh script should set all things at its own level.
A lower level source_me.sh script sets things it knows about.

## Typography rules:

### Rule #1 - CAPS_SNAKE_CASE

* CAPS_SNAKE_CASE is for exported shell ENV vars.
* lower_snake_case is for non-exported shell vars.

### Rule #2 - Things ending with _DIR

* Any var that end in _DIR is a directory.
* Under Microsoft rules - (visual studio) - these include a terminal slash.
* Under OUR rules, these do not include a terminal slash.
* And - we predomently use UNIX slashes for reasons of "quoting things".

* See below about things ending with _PY, _SH, _MAK, etc.

## PROJ_ROOT_DIR

This is the top most directory in your project.
Your top most GIT CLONE should be this directory.
More about this below.

## PROJ_HELPER_DIR

This is where many of the vast majority of helper scripts and Python
modules live It should generally be a GIT SUBMODULE to the
PROJ_ROOT_DIR.  And it should be located at

		`${PROJ_ROOT_DIR}/proj-helper-scripts`

Thus this file (ENV_VARS.md) should be found at:

```bash 
export PROJ_HELPER_DIR="${PROJ_ROOT_DIR}/proj-helper-scripts"

# This file is
${PROJ_HELPER_DIR}/docs/ENV_VARS.md
```

## PROJ_ROOT_DIR

This is the root directory of the project.

The LOSTARM package uses this package as a GIT SUBMODULE.

We do not intend to make this a standalone package that is released
and installed. There is a reason for this.

Often with Embedded (bare metal) development one needs to do a dozen
or two extra things with the SW package - often these things require
additional (python) scripts that do more things.

The intent is this:

    In your application is a small python stub and some JSON files
    that python stub 'orchistrates' what you want the python code to do.
    And the JSON files provide the settings in a convient file.

The intent is that that all the helpers you require are in the ${PROJ_HELPER_DIR}

## Generic variable Naming conventions

## PROJ_ - anything starting with PROJ

The goal of the PROJ_ set of names is to give us a clean namespace.

## PROJ_ROOT_DIR - is special. This is the root directory of your project.

All all file system paths are relative to this specific ENV Variable.

## What is LOSTARM_ then?

LOSTARM is a package that I (Duane) initially wrote about 20 years ago
(2007) for use with some ARM chip.  I still have this, and still
fiddle with it. I've decided to get off my lazy ass and make a new
real thing of it.

LOSTARM is generally the parent of this this PROJ_HELPER_DIR
Your project is generally a parent of this PROJ_HELPER_DIR

The Directory PROJ_HELPER_DIR is a shared git module.

## \*\_DIR - is always a directory

   Under Microsoft Visual Studio rules, a _DIR, ends with trailing
   backslash.  Under my rules, nope we are not doing that.

## BACK verses FORWARD slashes, MSYS and CYGWIN

   We always use forward slashes, always.
   Reason: Less non-sense escaping dos paths.

   Also, google search the tool: "cygpath"

   CYGWIN - is probably a very long way out.
   GITBASH - (msys) yes, that is a current target

   When supporting things on windows, We often need to refer to paths
   in different ways.  This is how we plan to solve that.

Example:

```bash
/c/users/duane -> is a windows MSYS path (aka: Git-Bash for windows)

c:\users\duane -> Is the windows path.

c:/users/duane -> ALl three of these mean the same thing.
```

   Using GITBASH (or CYGWIN) to convert one can type:

```bash
   INPUT: cygpath -a -u  c:\users\duane
   OUTPUT:  /c/users/duane
```

   or

```bash
   INPUT: cygpath -a -w  /c/users/duane
   OUTPUT: c:\users\duane
```

   or

```bash
   INPUT: cygpath -a -m c:\users\duane
   INPUT: cygpath -a -m /c/users/duane
   OUTPUT:   c:/users/duane
```

## Endings with EXE, SH, BAT, PY, PS1, TCL, or XTCL

   If the name ends with _EXE we assume it is an executable.
   Normally on Windows this is an .EXE file, hence the name.

   We know Linux does not use an executable extension, and _EXE is a
   windows thing.  But because windows is so ubiquitous, most of us know
   what EXE means.  So - to help self document variable names we use
   these naming conventions.

   On linux, this means it has the chmod+x bit set for any _EXE

   That rule does not extend to other _EXTENSIONS.

   Other names like *_BAT (windows), \_PY (python), \_PS1(powershell)
   and \_TCL (tcl/tk) are as you would expect.

   The term: XTCL exists to identify Xilinx XSCT tcl files.

   NOTE: We expect to execute each of these with their interpreter,
   which means we would normally execute these like this:

```bash
   1. bash ${PROJ_somename_SH} ... parameters ...
   2. cmd.exe /c ${PROJ_somename_BAT} ... parameters ...
   3. ${PROJ_PYTHON_EXE} ${PROJ_somename_PY} ... parameters ...
   4. powershell.exe ${PROJ_somename_PS1} ... parameters ...
   5. xsct ${PROJ_somename_XTCL} ... parameters ...
   6. tclsh ${PROJ_somename_TCL} ... parameters ...
```

About: \_TCL, and \_XTCL - generally we are not using TCL
anywhere. However, the current version of Xilinx I have and have used
has a tool called: 'xsct' which is a TCL based tool.

It is our understanding that starting with Xilinx 2026 that is
deprecated and they will be migrating to their custom version of
Python which has its own problems.



For details about PYTHON see:

   ```${PROJ_HELPER_DIR}/docs/ALL_ABOUT_PYTHON.md```

## PROJ_PYTHON_EXE - You must provide and set this

   See [${PROJ_HELPER_DIR}/docs/ALL_ABOUT_PYTHON.md](./ALL_ABOUT_PYTHON.md)

   In short, this is the absolute path to the python executable we use.
   This is a required variable you must provide.

   OFTEN this is set in your `${HOME}/.bashrc` file.

SYSTEM administrator - you can also set this "machine wide" by using
       /etc/profile.d, or /etc/environment.

## PROJ_HELPER_DIR - most often: ${PROJ_ROOT_DIR}/helper-scripts

   The LOSTARM system uses many helper scripts.
   All of these helper scripts are found via this variable.

## PROJ_BASH_DIR - most often: ${PROJ_HELPER_DIR}/bash

## PROJ_PYTHON_DIR - most often: ${PROJ_HELPER_DIR}/python

## PROJ_POWERSHELL_DIR - This is future,and would be ${PROJ_HELPER_DIR}/powershell.

## PROJ_TCL_DIR - This is future, and would be: ${PROJ_HELER_DIR}/tcl

   Today there are no TCL, PS1, or BAT scripts.

   If and when they appear, they should go in some place like:

   ```${PROJ_HELPER_SCRIPTS}/powershell```
