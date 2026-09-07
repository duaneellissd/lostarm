# These are the ENV Vars, and a road map to many things.

## GIT_ROOT_DIR

This GIT_ROOT_DIR is only used in *THIS* file. It is not used
anywhere. You should be able to find: ${GIT_ROOT_DIR}/.git

The OFFICIAL name is LOSTARM_ROOT_DIR

## LOSTARM_ROOT_DIR

This is the root directory of the project.

We currently do not "install" the LOSTARM package, it just exists as a directory structure on your hard drive that you point to with an env variable.

The intent is that the entire package is 100% self contained within that directory.

In 99.99% of the cases we believe LOSTARM_ROOT_DIR is exactly GIT_ROOT_DIR.

In your case you might only have a single cloned copy. For the maintainers (ie: ME), we might have two or three copies, yesterdays, today, an experiment. Etc.  By using this technique we can bounce between different instances of the tool.

As anyone who has used Xilinx tool in a professional setting, it is helpful to have the entire package installed as a single directory, ie: c:\xilinx\vivado\2019.1 and c:\xilinx\vivado\2024.2 are both installed and one often needs to switch back and forth depending on what you are doing.

Xilinx accomplishes this via ENV variables and a shell script called: settings64.sh (or .bat) in each directory.

## **If somebody on your IT team thinks this is dumb, tell them this:**

The facts of life in the embedded world is this: When changing any tool from version X to version X+1, sometimes the project no longer builds or no longer works. All engineering activity stops abruptly and completely.

Our IMS (Integrated Master Schedule) requires that it is trivial for us to be able to switch back to support a previous project, then switch forward to support a new or different project or even a third project. This is a hard requirement of our work flow.  This technique is perhaps the best way to solve that. It is so much simpler because each version is completely self contained within their own directories.

## Generic variable Naming conventions

## LOSTARM - anything starting with LOSTARM

The goal of the LOSTARM_ set of names is to give us a clean namespace.

Unless there is some other project or thing known as LOSTARM we should
be safe..

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
   1. bash ${LOSTARM_somename_SH} ... parameters ...
   2. cmd.exe /c ${LOSTARM_somename_BAT} ... parameters ...
   3. ${LOSTARM_PYTHON_EXE} ${LOSTARM_somename_PY} ... parameters ...
   4. powershell.exe ${LOSTARM_somename_PS1} ... parameters ...
   5. xsct ${LOSTARM_somename_XTCL} ... parameters ...
   6. tclsh ${LOSTARM_somename_TCL} ... parameters ...
```

About: \_TCL, and \_XTCL - generally we are not using TCL anywhere. However, the current version of Xilinx I have and have used has a tool called: 'xsct' which is a TCL based tool.

It is our understanding that starting with Xilinx 2026 that is deprecated and they will be migrating to their custom version of Python which has its own problems.

For details about PYTHON see:

   ```${LOSTARM_ROOT_DIR}/ALL_ABOUT_PYTHON.md```

## LOSTARM_PYTHON_EXE - You must provide and set this

   See [${LOSTARM_ROOT_DIR}/ALL_ABOUT_PYTHON.md](docs/ALL_ABOUT_PYTHON.md)

   In short, this is the absolute path to the python executable we use.
   This is a required variable you must provide.

   OFTEN this is set in your `${HOME}/.bashrc` file.

## LOSTARM_HELPER_DIR - most often: ${LOSTARM_ROOT_DIR}/helper-scripts

   The LOSTARM system uses many helper scripts.
   All of these helper scripts are found via this variable.

## LOSTARM_BASH_DIR - most often: ${LOSTARM_HELPER_DIR}/bash

## LOSTARM_PYTHON_DIR - most often: ${LOSTARM_HELPER_DIR}/python

## Today/Future

   Today there are no TCL, PS1, or BAT scripts.

   If and when they appear, they should go in some place like:

   ```${LOSTARM_HELPER_SCRIPTS}/powershell```
