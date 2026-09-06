# These are the ENV Vars, and a road map to many things.

## GIT_ROOT_DIR

This GIT_ROOT_DIR is only used in *THIS* file. It is not used
anywhere. You should be able to find: ${GIT_ROOT_DIR}/.git

The OFFICIAL name is LOSTARM_ROOT_DIR

## LOSTARM_ROOT_DIR

This is the root directory of the project.

In 99.99% of the cases, LOSTARM_ROOT_DIR is exactly GIT_ROOT_DIR.

## Generic variable Naming conventions:

## LOSTARM_* - anything starting with LOSTARM_

The goal of the LOSTARM_ set of names is to give us a clean namespace.

Unless there is some other project or thing known as LOSTARM we should
be safe..

## *_DIR - is always a directory.

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
   
```   
/c/users/duane	-> is a windows MSYS path (aka: Git-Bash for windows)

c:\users\duane	-> Is the windows path.

c:/users/duane	-> ALl three of these mean the same thing.

```

   Using GITBASH (or CYGWIN) to convert one can type:
```
   INPUT: cygpath -a -u  c:\users\duane
   OUTPUT:  /c/users/duane
```
   or
```
   INPUT: cygpath -a -w  /c/users/duane
   OUTPUT: c:\users\duane
```
   or
```
   INPUT: cygpath -a -m c:\users\duane
   INPUT: cygpath -a -m /c/users/duane
   OUTPUT:   c:/users/duane
```
   
## *_EXE, or *_SH, or *_BAT, or *_PY, or *_PS1, or *_XTCL

   If the name ends with _EXE we assume it is an executable.
   Normally on Windows this is an .EXE file, hence the name.

   We know Linux does not use an executable extension, and _EXE is a
   windows thing.  But because windows is so ubiquous, most of us know
   what EXE means.  So - to help self document variable names we use
   these naming conventions.

   On linux, this means it has the chmod+x bit set for any _EXE

   That rule does not extend to other _EXTENSIONS.

   Other names like *_BAT (windows), _PY (python), _PS1(powershell)
   and _TCL (tcl/tk) are as you would expect.

   NOTE: We expect to execute each of these with their interpreter,
   which means we would normally execute these like this:
   
```
   bash ${LOSTARM_somename_SH} ... parameters ...
   cmd.exe /c ${LOSTARM_somename_BAT} ... parameters ...
   ${LOSTARM_PYTHON_EXE} ${LOSTARM_somename_PY} ... parameters ...
   powershell.exe ${LOSTARM_somename_PS1} ... parameters ...
   xsct ${LOSTARM_somename_XTCL} ... parameters ...
   tclsh ${LOSTARM_somename_TCL} ... parameters ...
```

   About: _TCL, and _XTCL - generally we are not using TCL anywhere.
   However, the current version of Xilinx I have and have used has a
   tool called: 'xsct' which is a TCL based tool.

   It is my understanding that starting with Xilinx 2026 that is
   depricated and they will be migrating to their custom version of
   Python which has its own problems.

   For details about PYTHON see:

      ```${LOSTARM_ROOT_DIR}/ALL_ABOUT_PYTHON.md```
   
## LOSTARM_PYTHON_EXE - You must provide and set this.

   See ${LOSTARM_ROOT_DIR}/ALL_ABOUT_PYTHON.md

   In short, this is the absolute path to the python executable we use.
   This is a required variable you must provide.

   OFTEN this is set in your ${HOME}/.bashrc file.

## LOSTARM_HELPER_DIR - most often: ${LOSTARM_ROOT_DIR}/helper-scripts

   The LOSTARM system uses many helper scripts.
   All of these helper scripts are found via this variable.

## LOSTARM_BASH_DIR - most often: ${LOSTARM_HELPER_DIR}/bash

## LOSTARM_PYTHON_DIR - most often: ${LOSTARM_HELPER_DIR}/python

## Today/Future:

   Today there are no TCL, PS1, or BAT scripts.

   If and when they appear, they should go in some place like:

      ```${LOSTARM_HELPER_SCRIPTS}/powershell```
     
   