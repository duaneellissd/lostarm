"""
Q: What does this do?
A: It does three things.
A: First it creates a Python Virtual Environment (VENV)
A: Second it installs packages into the VENV.
A: Third it modifies the VENV by adding to the PYTHON PATH.
A: Fourth it modifies the PROJ_VSCODE_DIR adding python features.

Q: Why is this not a simple shell script instead of a python script?
A: Preforming steps 2 to 4 above is easier done in python.
"""

import sys
import os
import subprocess
import platform
import shutil
import json

def my_which( name ):
    path = os.environ.get('PATH')
    path = path.split(os.pathsep)
    tried = []
    for tmp in path:
        tmp = os.path.join( tmp, name )
        tried.append(tmp)
        if os.path.exists( tmp ):
            return (tmp,[])
    return (None,tried)
        

class UpdateCommon():
    def __init__(self):
        self.THIS_FILE=os.path.abspath( __file__ )
        self.THIS_DIR =os.path.dirname( self.THIS_FILE )
        
        # Get PROJ_PYTHON_EXE
        self.PROJ_PYTHON3_EXE=os.environ.get('PROJ_PYTHON3_EXE',None)
        if self.PROJ_PYTHON3_EXE is None:
            print "PROJ_PYTHON_EXE is not defined it is required"
            sys.exit(1))
        self.PROJ_PYTHON3_EXE = os.path.abspath( self.PROJ_PYTHON3_EXE )

        if sys.executable != self.PROJ_PYTHON3_EXE:
            print "PROJ_PYTHON_EXE=%s" % self.PROJ_PYTHON3_EXE
            print " sys.executable=%s" % sys.executable
            print "This is not consistent, please fix"
            sys.exit(1)

        self._verify_python_version()
            
        # Get the PROJ_PYTHON_DIR.
        self.PROJ_PYTHON_DIR=os.environ.get('PROJ_PYTHON_DIR',None)
        if self.PROJ_PYTHON_DIR is None:
            print "PROJ_PYTHON_DIR is not defined it is required"
            sys.exit(1)

        # Where is this script located?
        this_dir=os.path.dirname( os.path.abspath(__file__) )
        # this script should be where PROJ_PYTHON_DIR is located.
        if this_dir != self.PROJ_PYTHON_DIR:
            print "PROJ_PYTHON_DIR=%s" % self.PROJ_PYTHON_DIR
            print "       this_dir=%s" % this_dir
            print "This is not consistent, please fix"
            sys.exit(1)

        # Where does Python get its modules from?
        # Did user set this up ahead of time? 
        # Then we should honor that list of places
        self.PYTHONPATH=os.environ.get("PYTHONPATH",None)

        """
        I like to use PYCHARM, and PYCHARM does not always
        find/use the instance of Python.exe in my VENV.
        If this variable exists, PYCHARM will use that variable to find python.
        See if it exists.
        """
        self.PYCHARM_PYTHONPATH=os.environ.get("PYCHARM_PYTHONPATH",None)

        self.PROJ_VENV_DIR=os.environ.get("PROJ_VENV_DIR",None)
        if self.PROJ_VENV_DIR is None:
            print("PROJ_VENV_DIR is not defined it is required")

    def _verify_python_version(self):
        """
        Verify the version of python we found is at least 3.11
        """
        version_text = self._execute( [ self.PROJ_PYTHON3_EXE, "--version" ])
        parts = version_text.split(' ')
        if len(parts) != 2:
            print("expected: Python: SEMVER, got: %s" % version_text )
            sys.exit(1)
        semver = parts[1].split('.')
        if len(semver) != 3:
            print("expected PYTHON SEMVER (3numbers), got: %s" % version_text )
            sys.exit(1)
        ver_num = int(semver[0]) * 100
        ver_num = ver_num + int(semver[1])
        if ver_num < 311:
            print("We require python 3.11 or better, this is: %s" % version_text )
            sys.exit(1)
        # all is well.


    def verbose_print( self, level : int, msg :str ) -> None:
        """
        Print the message if the level is >= verbose, or if level = 0.
        """
        if (level==0) or (level <= self.VERBOSE):
            print(msg)


    def _execute( self, cmdline : list ) -> str:
        """
        Given a command line (array of args) execute these
        capture the output, check for errors etc.
        """
        self.verbose_print(0,"execute: %s" % " ".join(cmdline))
        result = subprocess.run( cmdline,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             text=True )
        self.verbose_print(0, result.stdout )
        if result.returncode != 0:
            self.verbose_print(0,"FAIL: ret code: %d" % result.returncode )
            sys.exit(result.returncode)
        self.verbose_print(1,result.stdout)
        return result.stdout

    def _run_requirements(self) -> None:
        """
        This effectively does: "pip -r requirements.txt" with a twist.
        Each platform we might run on has a different set of requirements.

        Example:
            We may be installing a local directory full of python packages.
            Those packages might be universal or a platform binary package.
            So we use the name: 'requirements-PLATFORM.txt' instead.
        """
        fn_tmp = "requirements.txt"
        w_or_l = platform.system()
        dirname = os.path.join( self.PROJ_PYTHON_DIR, "pip-%s" % platform.system )
        fn = os.path.join(dirname, fn_tmp )
        if not os.path.isfile( fn ):
            print("warning: missing %s" % fn)
            return
    
        tmp = [ self.PROJ_PYTHON3_EXE, "-m", "pip", "install", "-r", fn ]
        here = os.getcwd()
        os.chdir( dirname )
        self._execute( tmp )
        os.chdir( here )


    def create_venv( self ):
        if os.path.isdir( str(self.PROJ_VENV_DIR) ):
            shutil.rmtree( str(self.PROJ_VENV_DIR) )
        self._execute( [self.PROJ_PYTHON3_EXE, "-m", "venv", self.PROJ_VENV_DIR] )
        # the "str()" here makes pylance STFU otherwise these are not valid.
        self._update_python_exe()
        self._update_pythonpath()
        self._update_python_vars_XXX()
        self._run_requirements()
        self._update_activate_script()

    def _update_python_exe( self ):
        """
        Change our self.PROJ_PYTHON3_EXE to point at/into the VENV.
        """
        ht = platform.system()
        if ht == 'Windows'
            tmp = 'python3.exe'
        else:
            tmp = 'python3'
        tmp = str(os.path.join( str(self.PROJ_VENV_DIR), "bin", tmp ))
        if not os.access( tmp, os.X_OK ):
            print("%s: is not executable!" % tmp )
            sys.exit(1)
        self.PROJ_PYTHON3_EXE = tmp
        self.PYCHARM_PYTHONPATH = tmp

    def _update_pythonpath(self):
        """
        the user may or may not have set up a "PYTHONPATH"
        here we modify it by inserting OUR modules dir
        """
        our_path = os.path.join( self.PROJ_PYTHON_DIR, "modules" )
        if self.PYTHONPATH is None:
            self.PYTHONPATH = our_path
        else:
            places : list = self.PYTHONPATH.split(os.pathsep)
            if our_path not in places:
                places.insert(0, our_path )
            self.PYTHONPATH = os.pathsep.join(places)

    def _update_python_vars_XXX(self):
        """
        We place a "python_vars" in the VENV dir.
        This exists so that other things can get these vars
        in a simpleway, they can just source the script.
        Note that the script may already exist.
        """
        ht = platform.system()

        def do_update( fn : str, findme: str, attname ):
            value = self.__getattribute__( attname )
            _find_and_replace( fn, findme % attname, value )
        if ht in ("Linux", "Darwin"):
            this_fn = str(self.PYTHON_VARS_SH)
            print("Updating: %s" % this_fn )
            export_fmt = "export %s="
            do_update( this_fn, export_fmt, "PROJ_ROOT_DIR" )
            do_update( this_fn, export_fmt, "PROJ_PYTHON3_EXE" )
            do_update( this_fn, export_fmt, "PYTHONPATH")
            do_update( this_fn, export_fmt, "PYCHARM_PYTHONPATH" )
            if self.PROJ_VSCODE_EXE is not None:
                do_update( this_fn, export_fmt, "PROJ_VSCODE_EXE" )
            if self.PROJ_PYCHARM_EXE is not None:
                do_update( this_fn, export_fmt, "PROJ_PYCHARM_EXE" )
            os.chmod( this_fn, 0o777 )
        elif ht == "Windows":
            # batch files use "set NAME=VALUE"
            set_var="set %s="
            this_fn = str(self.PYTHON_VARS_BAT)
            print("Updating: %s" % this_fn )
            do_update( this_fn, set_var, "PROJ_PYTHON3_EXE")
            do_update( this_fn, set_var, "PYTHONPATH")
            do_update( this_fn, set_var, "PYCHARM_PYTHONPATH" )
            if self.PROJ_VSCODE_EXE is not None:
                do_update( this_fn, set_var, "PROJ_VSCODE_EXE" )
            if self.PROJ_PYCHARM_EXE is not None:
                do_update( this_fn, set_var, "PROJ_PYCHARM_EXE" )

            this_fn = str( self.PYTHON_VARS_PS1 )
            print("Updating: %s" % this_fn )
            # PS1 files use "$env:NAME=VALUE"
            set_var = "$env:%s="
            do_update( this_fn, set_var, "PROJ_PYTHON3_EXE" )
            do_update( this_fn, set_var, "PYTHONPATH")
            do_update( this_fn, set_var, "PYCHARM_PYTHONPATH" )
            if self.PROJ_VSCODE_EXE is not None:
                do_update( this_fn, set_var, "PROJ_VSCODE_EXE" )
            if self.PROJ_PYCHARM_EXE is not None:
                do_update( this_fn, set_var, "PROJ_PYCHARM_EXE" )



    def update_scripts(self):
        """
        To help our user, we create two scripts in the VENV BIN directory.
        One named: proj_vscode,
        Second: proj_pycharm

        Both setup some environment variables that are calculated by this script.
        Then launch the specific tool
        """
        ht = self.host_type()
        venv_dir = str(self.PROJ_VENV_DIR)
        if self.PROJ_VSCODE_EXE is None:
            print("WARNING: Could not find VSCODE executable")
            print("Please set/export the variable: PROJ_VSCODE_EXE")
        if self.PROJ_PYCHARM_EXE is None:
            print("WARNING Could not find PYCHARM executable")
            print("Please set/export the variable: PROJ_PYCHARM_EXE")

        if ht in ("Linux", "Darwin"):
            fn = os.path.join(venv_dir, "bin", "proj_vscode.sh")
            with( open(fn, "wt") ) as f:
                print("Creating: %s" % fn )
                f.write("#! /bin/bash\n")
                f.write("source %s\n" % self.PYTHON_VARS_SH )
                if self.PROJ_VSCODE_EXE is None:
                    f.write("echo ERROR VSCODE Was not found!\n")
                    f.write("Please set/export the variable: PROJ_VSCODE_EXE")
                    f.write("exit 1")
                else:
                    f.write('exec %s "${@}"\n' % self.PROJ_VSCODE_EXE )
            os.chmod( fn, 0o777 )
            fn = os.path.join( venv_dir, "bin", "proj_pycharm.sh" )
            with( open(fn, "wt") ) as f:
                print("Creating: %s" % fn )
                f.write("#! /bin/bash\n")
                f.write("source %s\n" % self.PYTHON_VARS_SH )
                if self.PROJ_PYCHARM_EXE is None:
                    f.write("echo ERROR PyCharm Was not found!\n")
                    f.write("Please set/export the variable: PROJ_PYCHARM_EXE")
                else:
                    f.write('exec %s "${@}"\n' % self.PROJ_PYCHARM_EXE )
            os.chmod( fn, 0o777 )
            return
        assert( ht == 'Windows' )
        fn = os.path.join( venv_dir, "Scripts", "proj_vscode.bat" )
        with ( open(fn, "wt") ) as f:
            print("Creating: %s" % fn )
            f.write("@echo off\n")
            f.write("call %s\n" % self.PYTHON_VARS_BAT )
            if self.PROJ_VSCODE_EXE is not None:
                f.write("%s\n" % self.PROJ_VSCODE_EXE)
            else:
                f.write("echo VSCODE was not found\n")
                f.write("Please set the variable: PROJ_VSCODE_EXE\n")

        fn = os.path.join( venv_dir, "Scripts", "proj_pycharm.bat" )
        with ( open(fn, "wt") ) as f:
            print("Creating: %s" % fn )
            f.write("@echo off\n")
            f.write("call %s\n" % self.PYTHON_VARS_BAT )
            if self.PROJ_PYCHARM_EXE is not None:
                f.write("%s\n" % self.PROJ_PYCHARM_EXE)
            else:
                f.write("echo PyCharm was not found\n")
                f.write("Please set the variable: PROJ_PYCHARM_EXE\n")





    def main( self ):
        self.create_venv()
        self.update_vscode()
        self.update_scripts()


def main( args : list[str] ):
    tool = VenvHelper( args )
    tool.main()

def normal_main(argv :  list[str]):
    main( argv )

def debug_main( argv : list[str] ):
    # this is here for testing only under a debugger
    os.environ[ "PROJ_PYTHON3_EXE"  ] = which_exe("python3")
    os.environ[ "PROJ_ROOT_DIR" ] = os.path.abspath("../..")
    tmp = os.path.join(os.environ['PROJ_ROOT_DIR'],".venv")
    main( [sys.argv[0],  tmp] )


def is_debugging():
    # Check if a trace function is active (used by pdb, PyCharm, etc.)
    has_trace = getattr(sys, 'gettrace', None) is not None and sys.gettrace() is not None

    # Check if the built-in breakpoint hook has been overwritten by an IDE/debugger
    has_breakpoint = sys.breakpointhook.__module__ != "sys"

    return has_trace or has_breakpoint

if __name__ == '__main__':
    if not is_debugging():
        normal_main( sys.argv )
    else:
        # inside PyCharm or Python Debugger.
        debug_main( sys.argv )
    sys.exit(0)

