# This helps set up a VENV for a MAC or LINUX or Windows.

# And helps with some other related debug things.
# general usage is:
#      python3 /path/to/vs_code_venv_helper.py  "${PATH_TO_VENV_DIR}"
# AKA: python3 /path/to/vs_code_venv_helper.py  .
import sys
import os
import subprocess
import platform
import shutil
import json

THIS_FILE=os.path.abspath(__file__)
THIS_DIR=os.path.dirname( THIS_FILE )

def _find_and_replace(filename: str, findme: str, value: str) -> None:
    """
    given a filename (typically a shell or bat or ps1 script)
    find a line stat starts with "findme", ie: "export FOO="
    And replace it with: "findme=VALUE", ie: export FOO=somevalue

    If the filename does not exist, create it.
    """
    result: list[str] = []
    in_lines = []
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            in_lines: list[str] = f.readlines()
    found = False
    for tmp in in_lines:
        tmp = tmp.rstrip()
        if tmp.startswith(findme):
            result.append("%s%s" % (findme, value))
            found = True
        else:
            result.append(tmp)
    if not found:
        result.append("%s%s" % (findme, value))
    with open(filename, "wt") as f:
        f.write("\n".join(result))
        f.write("\n")

def _update_dict( modified : bool, data : dict, key : str, val : (str|list|bool)) -> tuple[bool,dict]:
    """
    If key is not in the data dict, add it
    if value does not match, change it
    Return (modified, data )
    """
    if key not in data:
        modified = True
        data[key] = val
    elif isinstance( val, str ):
        if data[key] != val:
            modified = True
            data[key]=val
    elif isinstance( val, list ):
        modified = True
        existing = data[key]
        # If it is a string, make it a list.
        if isinstance( existing, str ):
            existing = [ existing ]
        assert( isinstance( existing, list ))
        combined = dict()
        for this_entry in val:
            combined[this_entry] = 1
        for this_entry in existing:
            combined[this_entry] = 1
        data[key] = list( combined.keys() )
    return modified,data

def which_exe( name : str ) -> str:
    """
    This is a wrapper/replacement for "shutil.which()"
    For some reason PyCharm thinks it is deprecated
    It seems pycharm is wrong
    """
    return shutil.which( name )



class VenvHelper(object):
    def __init__(self, args : list[str] ):
        if 'PROJ_ROOT_DIR' not in os.environ:
            print("FATAL: Missing environment variable 'PROJ_ROOT_DIR'")
            sys.exit(1)
        self.args = args
        """
        what level of log/debug are we creating, see self.verbose_print()
        The larger the number the more noise that is created.
        """
        self.VERBOSE = 0
        """
        What is the name of the VENV directory we are creating?
        (This is a command line parameter to this utility script)
        """
        self.LOSTARM_VENV_DIR : (str|None) = None

        self.parse_args(args)
        """
        Where is this script located?
        """
        tmp=os.path.dirname( os.path.abspath(__file__) )
        """this is located where this script is located"""
        self.PYTHON_HELPER_DIR=tmp
        """
        Where is PYCHARM installed?
        """
        tmp = os.environ.get("PROJ_PYCHARM_EXE", None)
        if tmp is None:
            tmp = which_exe( "pycharm" )
        self.PROJ_PYCHARM_EXE = tmp
        """
        Where is VSCODE installed?
        """
        tmp = os.environ.get("PROJ_VSCODE_EXE", None)
        if tmp is None:
            tmp = which_exe("code")
        self.PROJ_VSCODE_EXE = tmp

        tmp = os.path.join( self.PYTHON_HELPER_DIR, "spelling.json" )
        """ 
        Where do we keep our spelling dictionary?
        """
        self.SPELLING_WORDS_JSON_FN = tmp
        """
        Once read, our spelling word are a list here.
        """
        self.SPELLING_WORDS = []
        # go read our spelling words
        self.spelling_read_our_list()

        """
        Where does Python get its modules from?
        Did user set this up ahead of time? 
        Then we should honor that list of places
        """
        self.PYTHONPATH=os.environ.get("PYTHONPATH",None)

        """
        I like to use PYCHARM, and PYCHARM does not always
        find/use the instance of Python.exe in my VENV.
        If this variable exists, PYCHARM will use that variable to find python.
        See if it exists.
        """
        self.PYCHARM_PYTHONPATH=os.environ.get("PYCHARM_PYTHONPATH",None)

        """
        Sometimes, a system has multiple versions python installed.
        and we sometimes need to force a specific PYTHON_EXE file.
        SO - we assume/require you have set this variable
        For sort of same reasons as PYCHARM provides this escape hatch.
        """
        self.LOSTARM_PYTHON3_EXE: str | None = os.environ.get("LOSTARM_PYTHON3_EXE",None)
        if self.LOSTARM_PYTHON3_EXE is None:
            print("WARNING: Missing ENV Variable: LOSTARM_PYTHON3_EXE it is strongly suggested")
            tmp = which_exe( "python3" )
            if tmp is None:
                print("ERROR: Cannot find 'python3' in the path")
                tmp = sys.executable
            if tmp is None:
                print("FATAL: Tried: 'python3' and that failed too")
                sys.exit(1)
            # verify version of Python
            self.LOSTARM_PYTHON3_EXE = tmp
        elif not os.access( self.LOSTARM_PYTHON3_EXE, os.X_OK ):
            print("OS Env Variable: %s=%s" % ("LOSTARM_PYTHON3_EXE", self.LOSTARM_PYTHON3_EXE ) )
            print("FATAL: Not an executable")
            sys.exit(1)
        if (' ' in self.LOSTARM_PYTHON3_EXE) or ("\t" in self.LOSTARM_PYTHON3_EXE):
            # Yea, i have seen tabs in the path too! Dam those people.
            print("ERROR: Python3 is installed in a troublesome directory/path.")
            print("That path contains whitespace.  There must be no whitespace in that path")
            print("whitespace is either a tab of space")
            print("env var: LOSTARM_PYTHON3_EXE=%s" % self.LOSTARM_PYTHON3_EXE )
            sys.exit(1)
        self._verify_python_version()

        """
        Where is the root directory of the project.
        this is specified as an Environment variable.
        """
        self.PROJ_ROOT_DIR = os.environ.get("PROJ_ROOT_DIR", None)
        if self.PROJ_ROOT_DIR is None:
            print("Missing ENV variable: PROJ_ROOT_DIR, it is required")
            sys.exit(1)
        if not os.path.isdir( self.PROJ_ROOT_DIR ):
            print("%s: Not a directory" % self.PROJ_ROOT_DIR )
            sys.exit(1)
        """"
        To help others who use VSCODE, we will attempt to set things up for them too.
        We assume the .vscode directory is under the PROJ_ROOT_DIR
        """
        self.VSCODE_DIR = os.path.join(self.PROJ_ROOT_DIR, ".vscode")
        # it must be a directory, otherwise choke & puke up an error message
        # An assert is not appropriate her, but that is sort of what we are doing.
        if os.path.exists( self.VSCODE_DIR ):
            if not os.path.isdir( self.VSCODE_DIR ):
                print("%s: Exists and it is not a directory" % self.VSCODE_DIR )
                sys.exit(1)

        """
        Filename for vscode settings.json file
        """
        self.VSCODE_SETTINGS_JSON = os.path.join( self.VSCODE_DIR, "settings.json" )

        """
        VSCODE uses a "launch.json" file in the VSCODE_DIR
        """
        self.VSCODE_LAUNCH_JSON = os.path.join(self.VSCODE_DIR, "launch.json")

        """
        We will have our own modules that are not installed in the VENV.
        They are located here, in this directory.
        Maybe one day these will become "first class PIP modules on PyPpy
        But today they are not. So we put/keep them here.
        
        We could "pip install" them but we will not.
        
        Why? We want to be able to edit/update/adjust change these.
        It is simpler to not install them
        Otherwise you edit/change the installed module
        and never check in/commit your changes to these modules.
        """
        self.MODULES_DIR = os.path.join(self.PYTHON_HELPER_DIR, "modules")

        """
        We will create (or update) a "python_vars.sh" or "python_vars.bat"
        with updated variable names. We keep/place this in the VENV dir.
        We'll use that in many other places too.
        """
        ht = self.host_type()
        """ Python vars for BASH case """
        self.PYTHON_VARS_SH : (str|None) = None
        """ Python vars for Windows batch file case """
        self.PYTHON_VARS_BAT : (str|None) = None
        """ Python vars for Windows Power Shell file case """
        self.PYTHON_VARS_PS1 : (str|None) = None
        if ht in ("Linux","Darwin"):
            tmp = os.path.join( str(self.LOSTARM_VENV_DIR), "bin", "python_vars.sh")
            self.PYTHON_VARS_SH=tmp
            tmp= os.path.join( str(self.LOSTARM_VENV_DIR), "bin", "activate" )
            self.ACTIVATE_SH= tmp
        else:
            tmp = os.path.join( str(self.LOSTARM_VENV_DIR), "Scripts", "python_vars.bat")
            self.PYTHON_VARS_BAT=tmp
            tmp = os.path.join( str(self.LOSTARM_VENV_DIR), "Scripts", "python_vars.ps1")
            self.PYTHON_VARS_BAT=tmp
            tmp= os.path.join( str(self.LOSTARM_VENV_DIR), "Scripts", "activate.bat" )
            self.ACTIVATE_BAT= tmp
            tmp= os.path.join( str(self.LOSTARM_VENV_DIR), "Scripts", "activate.ps1" )
            self.ACTIVATE_PS1 = tmp


    def usage(self):
        """
        Print command line usage
        """
        print('usage: %s VENV_DIRNAME' % self.args[0])
        sys.exit(1)

    def parse_args( self, args: list[str] ):
        """ Skip the exe(script) name """
        self.args = args[1:]
        for tmp in self.args:
            if tmp == '-v':
                self.VERBOSE = self.VERBOSE + 1
                continue
            if self.LOSTARM_VENV_DIR is None:
                self.LOSTARM_VENV_DIR = tmp
                continue
            print("Multiple VENV dirs specified only 1 is allowed")
            self.usage()

    def _verify_python_version(self):
        """
        Verify the version of python we found is at least 3.11
        """
        version_text = self._execute( [ self.LOSTARM_PYTHON3_EXE, "--version" ])
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

    def host_type(self) -> str:
        tmp = platform.system()
        self.verbose_print(2,"host_type: %s" % tmp )
        return tmp

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
        fn_tmp = "requirements-%s.txt" % self.host_type()
        dirname = os.path.join( THIS_DIR, "pip-modules" )
        fn = os.path.join(dirname, fn_tmp )
        if not os.path.isfile( fn ):
            print("warning: missing %s" % fn)
            return
    
        tmp = [ self.LOSTARM_PYTHON3_EXE, "-m", "pip", "install", "-r", fn ]
        here = os.getcwd()
        os.chdir( dirname )
        self._execute( tmp )
        os.chdir( here )


    def create_venv( self ):
        if os.path.isdir( str(self.LOSTARM_VENV_DIR) ):
            shutil.rmtree( str(self.LOSTARM_VENV_DIR) )
        self._execute( [self.LOSTARM_PYTHON3_EXE, "-m", "venv", self.LOSTARM_VENV_DIR] )
        # the "str()" here makes pylance STFU otherwise these are not valid.
        self._update_python_exe()
        self._update_pythonpath()
        self._update_python_vars_XXX()
        self._run_requirements()
        self._update_activate_script()

    def _update_python_exe( self ):
        """
        Change our self.LOSTARM_PYTHON3_EXE to point at/into the VENV.
        """
        ht = self.host_type()
        if ht in ("Linux", "Darwin"):
            tmp = 'python3'
        else:
            tmp = 'python3.exe'
        tmp = str(os.path.join( str(self.LOSTARM_VENV_DIR), "bin", tmp ))
        if not os.access( tmp, os.X_OK ):
            print("%s: is not executable!" % tmp )
            sys.exit(1)
        self.LOSTARM_PYTHON3_EXE = tmp

    def _update_pythonpath(self):
        """
        the user may or may not have set up a "PYTHONPATH"
        here we modify it by inserting OUR modules dir
        """
        if self.PYTHONPATH is None:
            self.PYTHONPATH = self.MODULES_DIR
        else:
            places : list = self.PYTHONPATH.split(os.pathsep)
            if self.MODULES_DIR not in places:
                places.insert(0, self.MODULES_DIR)
            self.PYTHONPATH = os.pathsep.join(places)

    def _update_python_vars_XXX(self):
        """
        We place a "python_vars" in the VENV dir.
        This exists so that other things can get these vars
        in a simpleway, they can just source the script.
        Note that the script may already exist.
        """
        ht = self.host_type()

        def do_update( fn : str, findme: str, attname ):
            value = self.__getattribute__( attname )
            _find_and_replace( fn, findme % attname, value )
        if ht in ("Linux", "Darwin"):
            this_fn = str(self.PYTHON_VARS_SH)
            print("Updating: %s" % this_fn )
            export_fmt = "export %s="
            do_update( this_fn, export_fmt, "LOSTARM_PYTHON3_EXE" )
            do_update( this_fn, export_fmt, "PYTHONPATH")
            do_update( this_fn, export_fmt, "PYCHARM_PYTHONPATH" )
            if self.PROJ_VSCODE_EXE is not None:
                do_update( this_fn, export_fmt, "PROJ_VSCODE_EXE" )
            if self.PROJ_PYCHARM_EXE is not None:
                do_update( this_fn, export_fmt, "PROJ_PYCHARM_EXE" )

        elif ht == "Windows":
            # batch files use "set NAME=VALUE"
            set_var="set %s="
            this_fn = str(self.PYTHON_VARS_BAT)
            print("Updating: %s" % this_fn )
            do_update( this_fn, set_var, "LOSTARM_PYTHON3_EXE")
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
            do_update( this_fn, set_var, "LOSTARM_PYTHON3_EXE" )
            do_update( this_fn, set_var, "PYTHONPATH")
            do_update( this_fn, set_var, "PYCHARM_PYTHONPATH" )
            if self.PROJ_VSCODE_EXE is not None:
                do_update( this_fn, set_var, "PROJ_VSCODE_EXE" )
            if self.PROJ_PYCHARM_EXE is not None:
                do_update( this_fn, set_var, "PROJ_PYCHARM_EXE" )

    def _update_activate_script(self):
        txt = ""
        modified = False
        ht = self.host_type()
        found = False
        if ht in ("Linux", "Darwin"):
            with open( self.ACTIVATE_SH, "rt" ) as f:
                lines = f.readlines()
            result = []
            for tmp in lines:
                tmp = tmp.rstrip()
                if tmp.startswith("source "):
                    # the old source might be pointing at a different path
                    # So we look for the 'basename' not the abs path.
                    if os.path.basename(str(self.PYTHON_VARS_SH)) in tmp:
                        found = True
                        # The old one might be a different 'source' path
                        tmp = "source %s" % self.PYTHON_VARS_SH
                result.append(tmp)
            if not found:
                result.append("source %s" % self.PYTHON_VARS_SH)
            with open( self.ACTIVATE_SH, "wt" ) as f:
                print("Updating: %s" %  self.ACTIVATE_SH )
                f.write( "\n".join(result) )
                f.write("\n")
            return
        assert( ht == "Windows")
        with open( self.ACTIVATE_BAT, "rt" ) as f:
            lines = f.readlines()
        result = []
        for tmp in lines:
            tmp = tmp.rstrip()
            if tmp.startswith( "call " ):
                if os.path.basename(str(self.PYTHON_VARS_BAT)) in tmp:
                    found = True
                    tmp = "call %s" % self.PYTHON_VARS_BAT
            result.append( tmp )
        if not found:
            result.append( "call %s" % self.PYTHON_VARS_BAT )
        with open( self.ACTIVATE_BAT, "wt" ) as f:
            f.write( "\n".join(result) )
            f.write("\n")
        found = False
        with open( self.ACTIVATE_PS1, "rt" ) as f:
            lines = f.readlines()
        for tmp in lines:
            tmp = tmp.rstrip()
            if tmp.startswith("."):
                if os.path.basename(str(self.PYTHON_VARS_PS1)) in tmp:
                    found = True
                    tmp = ". %s" % self.PYTHON_VARS_PS1
                result.append(tmp)
        if not found:
            result.append(". %s" % self.PYTHON_VARS_PS1 )
        with open( str(self.PYTHON_VARS_PS1), "wt" ) as f:
            f.write( "\n".join(result) )
            f.write('\n')
        return

    def spelling_read_our_list( self ):
        """ populate the spelling words in the Python IDEs"""

        if not os.path.isfile( self.SPELLING_WORDS_JSON_FN ):
            self.SPELLING_WORDS = []
            return
        with open( self.SPELLING_WORDS_JSON_FN, "rt" ) as f:
            txt = f.read()
        try:
            data = json.loads( txt )
        except json.JSONDecodeError as E:
            print("%s:%d: Parse error loading spelling worlds %s" % (self.SPELLING_WORDS_JSON_FN, E.lineno, E.msg))
            sys.exit(1)
        if not isinstance( data, list ):
            print("%s:1: Expected a json LIST, file must start with a [" % self.SPELLING_WORDS_JSON_FN)
            sys.exit(1)
        self.SPELLING_WORDS = data

    def update_vscode(self):
        """
        VSCODE -we have to rewrite some json files in the .vscode directory.
        """
        self._update_vscode_launch()
        # Then the python setup too.
        self._vscode_python_settings()

    def update_scripts(self):
        """
        To help our user, we create two scripts in the VENV BIN directory.
        One named: proj_vscode,
        Second: proj_pycharm

        Both setup some environment variables that are calculated by this script.
        Then launch the specific tool
        """
        ht = self.host_type()
        venv_dir = str(self.LOSTARM_VENV_DIR)
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

    def _update_vscode_launch(self):
        """
        We want to support using VSCODE to debug python stuff.
        So we need to tell VSCODE about our VENV eetc.
        """
        fn_launch = self.VSCODE_LAUNCH_JSON
        modified = False
        if os.path.isfile( fn_launch ):
            txt = ""
            with open( fn_launch, "rt" ) as f:
                txt = f.read()
            try:
                data = json.loads( txt )
            except json.JSONDecodeError as E:
                print("%s:%d: Parse error: %s" % (fn_launch, E.lineno, E.msg ))
                sys.exit(1)
        else:
            modified = True
            # Start with an empy dict if the file does not exist.
            data = {}
        ok=False
        # basic version check.
        if 'version' in data:
            tmp=data['version']
            if tmp == "0.2.0":
                ok=True
        else:
            # Then assume it is v0.2.0
            data['version']="0.2.0"
            ok=True
        if not ok:
            self.verbose_print(0,"%s: version is not 0.2.0" % fn_launch )
            sys.exit(1)
        la_cfg = dict()
        our_name="PROJ: Python"
        la_cfg['name'] = our_name
        la_cfg['type'] = "debugpy"
        la_cfg['request']="launch"
        la_cfg['program']="${file}"
        la_cfg['console']="integratedTerminal"
        # Tell VS Code where Python is located
        la_cfg['python'] = self.LOSTARM_PYTHON3_EXE
        # This lets us debug things in the python/modules directory.
        la_cfg['justMyCode']=False
        # No we do not do this
        #  la_cfg['cwd']=os.path.dirname( VSCODE_DIR )
        la_cfg['env'] = dict()
        la_cfg['env']['PYTHONPATH'] = self.PYTHONPATH
        la_cfg['env']['LOSTARM_PYTHON3_EXE']=self.LOSTARM_PYTHON3_EXE
    
        # Make sure we have something to iterate over
        if 'configurations' not in data:
            data['configurations'] = []
            modified = True
        # See if it already exists.
        found = -1
        # this is an array, we put ours at the front
        other_cfgs = [ la_cfg ]
        # Then insert all others after ours
        for tmp in data['configurations']:
            if tmp['name'] == la_cfg['name']:
                # Skip over our self.
                continue
            other_cfgs.append(tmp)
        #
        data['configurations'] = other_cfgs
        # Save updated file
        dname = os.path.dirname( self.VSCODE_LAUNCH_JSON )
        if not os.path.isdir( dname ):
            os.makedirs( dname )
        with open( self.VSCODE_LAUNCH_JSON, "wt" ) as f:
            print("Updating: %s" % self.VSCODE_LAUNCH_JSON )
            f.write( json.dumps( data, indent=4 ) )

    def _vscode_spelling_words( self, modified : bool, data : dict) -> tuple[bool,dict]:
        """
        We have our list of 'spelling words' in self.SPELLING_WORDS
        we wish to seed these into vscode cSpell.words
        """
        # get existing word list that vscode knows about
        key='cSpell.words'
        if key not in data:
            data[key]=[]
            modified = True
        # This is a list
        vscode_words = data[key]
        # ours is a list
        # combine the lists and remove duplicates via "set()"
        self.SPELLING_WORDS = list(set( data[key] + self.SPELLING_WORDS ))
        # Copy ours to the vscode list
        data[key] = self.SPELLING_WORDS[:]
        return modified, data


    def _vscode_python_settings(self):
        """
        Add detail about python to the vscode settings file
        """
        fn = str(self.VSCODE_SETTINGS_JSON)
        modified = False
        # attempt to modify the existing.
        if os.path.isfile( fn ):
            txt = None
            with open(fn,"rt") as f:
                txt = f.read()
            self.verbose_print(1,"Read: %s\n%s\n" % (fn,txt))
            data = json.loads( txt )
            assert( isinstance( data, dict ))
        else:
            # does not exist, so create
            modified = True
            data = dict()
        assert( isinstance(data,dict))
        key="python.defaultInterpreterPath"
        (modified, data) = _update_dict( modified, data, key, str(self.LOSTARM_PYTHON3_EXE) )
        key = "python.linting.pylintEnabled"
        (modified, data) = _update_dict( modified, data,key, True )
        key = 'python.linting.enabled'
        (modified, data) = _update_dict( modified,data,key,True)
        key = 'python.pythonPath'
        (modified, data) = _update_dict( modified, data,key, str(self.LOSTARM_PYTHON3_EXE) )
        key = "python.analysis.extraPaths"
        (modified, data) = _update_dict( modified, data, key, [ self.MODULES_DIR ])
        key =   "python.analysis.typeCheckingMode"
        (modified, data) = _update_dict( modified, data, key, "strict" )

        (modified, data) = self._vscode_spelling_words( modified, data )
        dir_name = os.path.dirname( fn )
        if not os.path.isdir(dir_name):
            modified = True
            os.makedirs(dir_name)
        if modified:
            with open(fn,"wt" ) as f:
                json.dump( data, f, indent=4 )
        self.verbose_print(1,"Updated: %s" % fn )


    def main( self ):
        self.create_venv()
        self.update_vscode()
        self.update_scripts()


def main( args : list[str] ):
    tool = VenvHelper( args )
    tool.main()

def normal_main(argv :  list[str]):
    main( argv )

def debug_main( _ : list[str] ):
    # this is here for testing only under a debugger
    os.environ[ "LOSTARM_PYTHON3_EXE"  ] = which_exe("python3")
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

