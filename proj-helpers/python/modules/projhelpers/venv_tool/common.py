
class UpdateCommon():
    """
    This class is used by:
    create_venv.py
    and by update_venv.py
    and by update_vscode.py
    and by update_pcharm.py 
    """
    
    def __init__(self, **kwargs):
        self.VERBOSE = 0 # Set verbosity level = 0
        for tmp in sys.argv:
            # See if -v exists in the command line.
            if tmp == '-v':
                self.VERBOSE = self.VEBOSE + 1
            
        # STEP 1 - where are we located?
        self.THIS_FILE=os.path.abspath( __file__ )
        self.THIS_DIR =os.path.dirname( self.THIS_FILE )


        # STEP 2 - Get PROJ_PYTHON_EXE
        self.PROJ_PYTHON_EXE=os.environ.get('PROJ_PYTHON_EXE',None)
        if self.PROJ_PYTHON_EXE is None:
            print("PROJ_PYTHON_EXE is not defined it is required")
            sys.exit(1)
        self.PROJ_PYTHON_EXE = os.path.abspath( self.PROJ_PYTHON_EXE )

        # And is PROJ_PYTHON_EXE the same as our executable?
        # these must be the same.
        # Do these strings as lower cause C:\ verses c:\ on windblows.
        if sys.executable.lower() != self.PROJ_PYTHON_EXE.lower():
            print("PROJ_PYTHON_EXE=%s" % self.PROJ_PYTHON_EXE)
            print(" sys.executable=%s" % sys.executable)
            print("This is not consistent, please fix")
            sys.exit(1)

        # STEP 3 - Make sure we are on Python 3.10 or better.
        # Note: Python3.10 was released Oct 24, 2022 have updated
        # MOST - if not all DISTROS have updated so we target at least that.
        # And generally do not require more then 3.6 or 3.7
        # I could be wrong.. but 3.7 was released 9 years ago Jun 27, 2018
        print("Python version is: %s" % sys.version)
        version = (sys.version_info[0] * 100) + sys.version_info[1]
        if version < 310:
            print("Python must be 3.10 or better. Sorry\n")
            sys.exit(1)
            
        # Get the PROJ_PYTHON_DIR.
        # This is where our PROJ_HELPER_SCRIPTS modules are located.
        self.PROJ_PYTHON_DIR=os.environ.get('PROJ_PYTHON_DIR',None)
        if self.PROJ_PYTHON_DIR is None:
            print("PROJ_PYTHON_DIR is not defined it is required")
            sys.exit(1)

        # Where is this script located?
        # this script should be at the top of PROJ_PYTHON_DIR
        if self.THIS_DIR.lower() != self.PROJ_PYTHON_DIR.lower():
            print("PROJ_PYTHON_DIR=%s" % self.PROJ_PYTHON_DIR)
            print("       this_dir=%s" % self.THIS_DIR )
            print("This is not consistent, please fix")
            sys.exit(1)

        # PYTHONPATH is the standard env variable PYTHON uses
        # to look for modules.

        our_module_dir=os.path.join( self.THIS_DIR, 'modules' )
        self.PYTHONPATH=os.environ.get("PYTHONPATH",None)
        if self.PYTHONPATH is None:
            self.PYTHONPATH=[]
        ht = patform.system()
        ignore_case = False
        if ht in ('Windows','Darwin'):
            # must ignore case
            ignore_case = True
        elif ht == 'Linux':
            # Case matters on
            ignore_case = False
        else:
            print("Unknown host type: %s, expected one of: Windows, Darwin, Linux\n" % ht )
            sys.exit(1)
            
        found = false
        for tmp in self.PYTHONPATH:
            if found:
                break
            A = tmp
            B = our_module_dir
            if ignore_case:
                found = (A.lower() == B.lower())
            else:
                found = (A == B)
        # If not found then insert at front.
        if not found:
            self.PYTHONPATH.insert(0, our_module_dir )
        """
        I like to use PYCHARM, and PYCHARM does not always find the VENV
        BUT per PYCHARM docs, if PYCHARM_PYTHONPATH exists then it points
        to the PYTHON executable it should use.
        See if it exists.
        """
        self.PYCHARM_PYTHONPATH=os.environ.get("PYCHARM_PYTHONPATH",None)
        if self.PYCHARM_PYTHONPATH is None:
            # default it just in case.
            self.PYCHARM_PYTHONPATH = self.PROJ_PYTHON_EXE

        # Externally something should have provded PROJ_VENV_DIR
        # This is where our VENV will be created
        # Other things like update_XXXXX.py need to know its location.
        self.PROJ_VENV_DIR=os.environ.get("PROJ_VENV_DIR",None)
        if self.PROJ_VENV_DIR is None:
            print("PROJ_VENV_DIR is not defined it is required")
        # In the case of "create_venv.py" PROJ_VENV_DIR might not exist yet.

    def dequote( s : str ) -> str:
        """
        For windows things sometimes need to be quoted.
        """

        # does the string start with a quote?
        if (s[0] not in ('"',"'")):
            return s
        # Ok it starts with a quote
        # make sure it ends with the same quote
        if s[0] != s[-1]:
            print("Invalid quoted string: %s" % s )
            sys.exit(1)
            
        # remove quote at start/end
        s = s[1:-1]
        # return the dequoted text.
        return s
        
    def quote_if_needed( self, s : str ) -> str:
        # if the string starts with a quote
        if ' ' not in s:
            return s
        
        s = '"' + s + '"'
        return s

    def windows_quote( self, s : str ) -> str :
        s = self.dequote(s)
        if platform.system() == 'Windows':
            s = self.quote_if_needed()
        return s
    
    def verbose_print( self, level : int, msg :str ) -> None:
        """
        Print the message if the level is >= verbose, or if level = 0.
        """
        if (level==0) or (level <= self.VERBOSE):
            print(msg)
