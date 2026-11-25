# DO NOT import more then these three modules.
import os
import sys
import shutils

PYTHON_MIN_VERSION=310
#----------------------------------------
# WHY NOT? We want this file to "reasonably" work with old pythons.
#
# EXAMPLE:
#
#   If the user is running a REALLY old version of python (ie: 2.7)
#   Then we want this script to DIE with "human friendly" error message
#   We do not want: "python vomit" ever.
#   Python Vomit might be the pythonic way of doing things
#   BUT Python Vomit is a bad thing for a noobie human to deal with.
#
# Thus we have these two rules:
#--------------------------------------------------
# RULE: Python2.7 shall be able to PARSE the ENTIRE file without error.
#                 PARSE means PARSE only.
#                 PARSE does not mean EXECUTE the entire file.
#
# RULE: Python2.7 shall be able to begin executing this file
#                 BUT the checks below discover Python <= PYTHON_MIN_VERSION
#
# RULE: Nice to have, an earlier version of python?
#       I choose Python2.7 as a line in the sand to draw this line.
#
# RULE: if <= PYTHON_MIN_VERSION then error messages shall be printed.
#
# RULE: All error messages shall not be PYTHON VOMIT.
#       PYTHON VOMIT is defined as a crash, a exception back trace, etc.
#
# RULE: Python(PYTHON_MIN_VERSION) or better can exist under these rules:
#       Rule #1 - the above rules work.
#       Rule #2 - Python(PYTHON_MIN_VERSION) things can exist only AFTER
#                 the point of DEMARCATION.
#--------------------------------------------------

THIS_FILE=os.path.abspath( __file__ )
THIS_DIR=os.path.dirname( THIS_FILE )

#--------------------------------------------------
# We do not know if we are under Python2 or Python3
# So this exists.
#--------------------------------------------------
def my_print(msg):
    # we use this so it works nicely in python2 .
    sys.stdout.write( msg )
    sys.stdout.write( '\n' )
    sys.stdout.flush()

#--------------------------------------------------
# Just print and die.
#--------------------------------------------------
def fatal( msg ):
    # print where this comes from
    my_print("%s: FATAL ERROR" % THIS_FILE )
    # so our victim can go spelunking in the maze of files
    # and figure out easily where the message came from.
    # This is part of our "trail of bread crumbs".
    my_print("FATAL: %s\n" % msg )
    sys.exit(1)

#--------------------------------------------------
# Check python version, this stops <= PYTHON_MIN_VERSION
#--------------------------------------------------
v = (sys.version_info[0] * 100) + (sys.version_info[1])
if v < PYTHON_MIN_VERSION:
    my_print("this is python: %s\n" % sys.python_version )
    fatal("This requires python %s or better\n" % PYTHON_MIN_VERSION )

#--------------------------------------------------
# This is our line of demarcation.
# *** DEMARCATION *** DEMARCATION *** DEMARCATION *** DEMARCATION ***
# This is our line of demarcation.
#--------------------------------------------------
# From here on, Python2.7 must be able to "parse" this
# Python2.7 is not intended to RUN this.
# The above check verfied that we are at least >= PYTHON_MIN_VERSION.

#--------------------------------------------------
# We must not be inside a venv.
#--------------------------------------------------
if sys.prefix != sys.base_prefix:
    # NOTE: "sys.prefix" exists in 2.7
    #       "sys.base_prefix" does not
    # BUT we have our 3.10 check above!
    fatal("This should not be run from within a VENV\n")

#--------------------------------------------------
# We require a number of variables to exist.
# This helps verify they exist.
#--------------------------------------------------
def required_var( name ):
    """
    If the name does not exist just die.
    if the name does exist - return the value.
    """
    if name not in os.environ:
        fatal("ENV var: %s is missing, it is required\n" % name )
    return os.environ[name]


#--------------------------------------------------
# Determine if PROJ_ROOT_DIR is valid or not.
#--------------------------------------------------
PROJ_ROOT_DIR=required_var( 'PROJ_ROOT_DIR' )
# tests..
tmp1=os.path.basename( THIS_FILE )
tmp2 = os.path.join( PROJ_ROOT_DIR, tmp1 )
# windows: c:\ is the same as C:\ so lowercase all things.
tmp3 = tmp1.lower()
tmp4 = THIS_FILE.lower()
if tmp3 != tmp4:
    my_print("    THIS_FILE: %s" % THIS_FILE} )
    my_print("PROJ_ROOT_DIR: %s" % PROJ_ROOT_DIR})
    my_print("     expected: %s" % tmp1)
    my_print("       actual: %s" % THIS_FILE )
    fatal("this is not consistent, fix this")
    sys.exit(1)

#----------------------------------------
# We expect/require PROJ_HELPER_DIR to be set
# normally this is set by ${PROJ_ROOT_DIR}/source_me.sh
#----------------------------------------
PROJ_HELPER_DIR=required_var( 'PROJ_HELPER_DIR' )

PROJ_PYTHON_EXE=required_var( 'PROJ_PYTHON_EXE' )

PROJ_VENV_DIR=required_var( 'PROJ_VENV_DIR' )

#----------------------------------------
# create our VENV.
# BUT first check if "--force" is specified.
#----------------------------------------
if ('-force' in sys.argv) or ('--force' in sys.argv):
    FORCE=True
else:
    FORCE=False

if os.path.exits( PROJ_VENV_DIR ):
    if FORCE:
        try:
            shutil.rmtree( PROJ_VENV_DIR ):
        except:
            fatal("Cannot remove %s" % PROJ_VENV_DIR )
    else:
        my_print("%s: Already exists" % PROJ_VENV_DIR )
        my_print("Use --force to delete & replace it")
else:
    pass
    # it does not exist - so we can just create it.

def execute_cmdline( cd_dir, cmdline ):
    old_dir = os.getcwd()
    my_print("cd %s" % cd_dir )
    os.chdir( cd_dir )
    my_print(cmdline)
    r = os.system( cmdline )
    if r != 0:
        my_print("PROJ_PYTHON_EXE: %s" % PROJ_PYTHON_EXE )
        my_print("  PROJ_VENV_DIR: %s" % PROJ_VENV_DIR )
        my_print("cd %s" % PROJ_ROOT_DIR)
        my_print("%s" % cmdline )
        my_print("")
        fatal("The above failed.")
    else:
        my_print("Success")
    os.chdir( old_dir )

# this creates the VENV.
cmdline = '%s -m venv "%s"' % (PROJ_PYTHON_EXE, PROJ_VENV_DIR)
execute_cmdline( cmdline )

if platform.system() == 'Windows':
    PROJ_PYTHON_EXE=os.path.join( PROJ_VENV_DIR, 'Scripts', 'python.exe')
else:
    PROJ_PYTHON_EXE=os.path.join( PROJ_VENV_DIR, 'bin', 'python')
os.environ['PROJ_PYTHON_EXE']=PROJ_PYTHON_EXE

PROJ_PYTHON_DIR=os.path.join(PROJ_HELPER_DIR, "python" )

# RUN PIP to install modules.
my_print("cd %s" % PROJ_PYTHON_DIR )
os.chdir( PROJ_PYTHON_DIR )
cmdline = '%s %s' % (PROJ_PYTHON_EXE, 'run_pip.py' )
execute_cmdline( cmdline )

#----------------------------------------
# update the venv directory (modify the activate scripts)
#----------------------------------------
cmdline = "%s %s" % (PROJ_PYTHON_EXE, 'update_venv.py' )
execute_cmdline( cmdline )

#----------------------------------------
# I used VSCODE, as do many others.
#----------------------------------------
cmdline = "%s %s" % (PROJ_PYTHON_EXE, 'update_vscode.py')
execute_cmdline( cmdline )

#----------------------------------------
# I also use PYCHARM, as do many others.
#----------------------------------------
cmdline = "%s %s" % (PROJ_PYTHON_EXE, 'update_pycharm.py')
execute_cmdline( cmdline )


"""
Q: What does this do?
A: First it creates a Python Virtual Environment (VENV)
A: Second, this installs pip packages into the VENV.
A: NOTE: OTHER SCRIPTS that Run AFTER this do the following:
A: Script: update_vscode.py - updates the VSCODE directory and creates ${PROJ_ROOT_DIR}/run_vscode.sh
A: Script: update_pycharm.py - updates things for Pycharm and creates ${PROJ_ROOT_DIR}/run_pycharm.sh

Q: Why is this not a simple script?
A: doing this in python is more portable across Windows, Linux and Mac
"""

import sys
import os
import platform

def fatal( msg ):
    print( msg )
    sys.exit(1)

PROJ_PYTHON_EXE = ""
PROJ_VENV_DIR= ""
PROJ_HELPERSCRIPTS_DIR=""

def get_var( name ):
    if name not in os.environ:
        printf("%s: env var is not defined it is required\n" % name)
        sys.exit(1)
    globals()[name] = os.environ[name]

def my_chdir( fullpath ) -> None:
    """
    Handle the Windows case where the new dir is on another disk.
    ie:  you are on c:/users/YOURNAME, new place is M:/other/place
    """
    fullpath = os.path.abspath(fullpath)
    if platform.system() == 'Windows':
        # Drives are the first 3 bytes.
        drive = fullpath[0:3] # ie: Y:/
        os.chdir( drive )
    os.chdir( fullpath )


def execute_python( cwd, cmdline : list[str] ) -> None:
    """
    Given a list of parameters for PYTHON_EXE - execute it.
    """
    cmdline_text = "%s %s" % (PROJ_PYTHON_EXE, " ".join(cmdline))
    # remember the old directory.
    old_cwd = os.getcwd()
    # Switch to the specified directory.
    my_chdir( cwd )
    # Execute.
    r = os.system( cmdline_text )
    # return to the old directory.
    my_chdir( old_cwd )
    # Die if that execution did not work.
    if r != 0:
        print("Execute Failed, exit code: %d command was:" % r )
        print("cd %s" % cwd )
        print("%s" % cmdline_text )
        fatal("Exit code was: %d" % r )

def update_PROJ_PYTHON_EXE() -> None:
    if platform.system() == 'Windows':
        PROJ_PYTHON_EXE = os.path.join( PROJ_VENV_DIR, "Scripts", "python.exe" )
    else:
        PROJ_PYTHON_EXE = os.path.join( PROJ_VENV_DIR, "bin", "python" )

def create_venv():
    args = []
    args.append( "-m" )
    args.append( "venv" )
    args.append( PROJ_VENV_DIR )
    execute_python( os.getcwd(), args)

def main( self ):
    create_venv()

def main():
    get_var( 'PROJ_PYTHON_EXE' )
    get_var( 'PROJ_VENV_DIR' )
    get_var( 'PROJ_HELPERSCRIPTS_DIR' )

    create_venv( ar
    tool = VenvHelper( args )
    tool.main()

def is_debugging():
    # Check if a trace function is active (used by pdb, PyCharm, etc.)
    has_trace = getattr(sys, 'gettrace', None) is not None and sys.gettrace() is not None

    # Check if the built-in breakpoint hook has been overwritten by an IDE/debugger
    has_breakpoint = sys.breakpointhook.__module__ != "sys"

    return has_trace or has_breakpoint

if __name__ == '__main__':
    main()
    sys.exit(0)
