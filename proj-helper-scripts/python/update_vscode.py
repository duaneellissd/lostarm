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
            tmp = os.path.join( str(self.PROJ_VENV_DIR), "bin", "python_vars.sh")
            self.PYTHON_VARS_SH=tmp
            tmp= os.path.join( str(self.PROJ_VENV_DIR), "bin", "activate" )
            self.ACTIVATE_SH= tmp
        else:
            tmp = os.path.join( str(self.PROJ_VENV_DIR), "Scripts", "python_vars.bat")
            self.PYTHON_VARS_BAT=tmp
            tmp = os.path.join( str(self.PROJ_VENV_DIR), "Scripts", "python_vars.ps1")
            self.PYTHON_VARS_BAT=tmp
            tmp= os.path.join( str(self.PROJ_VENV_DIR), "Scripts", "activate.bat" )
            self.ACTIVATE_BAT= tmp
            tmp= os.path.join( str(self.PROJ_VENV_DIR), "Scripts", "activate.ps1" )
            self.ACTIVATE_PS1 = tmp

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
        (modified, data) = _update_dict( modified, data, key, str(self.PROJ_PYTHON3_EXE) )
        key = "python.linting.pylintEnabled"
        (modified, data) = _update_dict( modified, data,key, True )
        key = 'python.linting.enabled'
        (modified, data) = _update_dict( modified,data,key,True)
        key = 'python.pythonPath'
        (modified, data) = _update_dict( modified, data,key, str(self.PROJ_PYTHON3_EXE) )
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
        la_cfg['python'] = self.PROJ_PYTHON3_EXE
        # This lets us debug things in the python/modules directory.
        la_cfg['justMyCode']=False
        # No we do not do this
        #  la_cfg['cwd']=os.path.dirname( VSCODE_DIR )
        la_cfg['env'] = dict()
        la_cfg['env']['PYTHONPATH'] = self.PYTHONPATH
        la_cfg['env']['PROJ_PYTHON3_EXE']=self.PROJ_PYTHON3_EXE
    
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
    
