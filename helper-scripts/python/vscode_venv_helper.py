# This helps setup a VENV for a MAC or LINUX 
# And and helps with some other related debug things.
# general usage is:
#      "python3 /path/to/vs_code_venv_helper.py  PROJECTROOTDIR"
# AKA: "python3 /path/to/vs_code_venv_helper.py  ."
import sys
import os
import subprocess
import platform
import shutil
import json

VERBOSE = 0
PYTHON_PATH=""
PYTHON3_EXE=shutil.which('python3')
PIP_EXE= []
PROJ_ROOT_DIR=""
VENV_DIR=""
VSCODE_DIR=""
VSCODE_LAUNCH_JSON=""
MODULES_DIR=""
LOSTARM_PYTHON_SETTINGS_SH=""
ACTIVATE_SH=""

def verbose_print( level : int, msg :str ) -> None:
    if (level <= VERBOSE ):
        print(msg)

def startswith( parent, child ):
    if child.startswith( parent ):
        return
    print("WRONG: parent: %s" % parent )
    print("        child: %s" % child )
    sys.exit(1)
        
def set_proj_root_dir( path ):
    global PROJ_ROOT_DIR
    PROJ_ROOT_DIR=os.path.abspath(path)
    global VENV_DIR
    VENV_DIR=os.path.join( PROJ_ROOT_DIR, '.venv')
    startswith( PROJ_ROOT_DIR, VENV_DIR )
    global VSCODE_DIR
    VSCODE_DIR=os.path.join( PROJ_ROOT_DIR, '.vscode' )
    startswith( PROJ_ROOT_DIR,VSCODE_DIR)
    global VSCODE_LAUNCH_JSON
    VSCODE_LAUNCH_JSON=os.path.join(VSCODE_DIR,"launch.json")
    startswith( PROJ_ROOT_DIR, VSCODE_LAUNCH_JSON )
    
    global VSCODE_SETTINGS_JSON
    VSCODE_SETTINGS_JSON=os.path.join(VSCODE_DIR,"settings.json")
    global MODULES_DIR
    this_dir=os.path.dirname( os.path.abspath( __file__ ) )
    startswith( PROJ_ROOT_DIR, this_dir )
    MODULES_DIR=os.path.join(this_dir,'modules')
    global LOSTARM_PYTHON_SETTINGS_SH
    LOSTARM_PYTHON_SETTINGS_SH=os.path.join( VENV_DIR, "lostarm_python.sh" )
    startswith( PROJ_ROOT_DIR, LOSTARM_PYTHON_SETTINGS_SH )
    global ACTIVATE_SH
    ACTIVATE_SH=os.path.join( VENV_DIR, "bin", 'activate')
    startswith( PROJ_ROOT_DIR, ACTIVATE_SH )
    
def host_type() -> str:
    
    tmp = platform.system()
    verbose_print(1,"host_type: %s" % tmp )
    return tmp

def execute( cmdline : list ):

    verbose_print(0,"execute: %s" % " ".join(cmdline))
    result = subprocess.run( cmdline,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             text=True )
    verbose_print(0, result.stdout )
    if result.returncode != 0:
        print("FAIL: ret code: %d" % result.returncode )
        sys.exit(result.returncode)
    verbose_print(1,result.stdout)

def get_exes():
    global PIP_EXE
    global PYTHON3_EXE
    PIP_EXE=None
    PYTHON3_EXE=None
    
    t = os.path.join( VENV_DIR, "bin", "python3" )
    if os.path.isfile( t ):
        PYTHON3_EXE=t
    else:
        PYTHON3_EXE=shutil.which('python3')
    PIP_EXE = [ PYTHON3_EXE, '-m', "pip" ]
    
    # We do not use pip in the venv dir
    # We want to be more specific about the instance
    if (PYTHON3_EXE is None) or (PIP_EXE is None):
        print("cannot find python3 or pip")
        sys.exit(1)
    verbose_print(1,"PYTHON3_EXE=%s" % PYTHON3_EXE)
    verbose_print(1,"PIP_EXE=%s" % PIP_EXE)
        
def run_requirements() -> None:
    fn = os.path.join(PROJ_ROOT_DIR,"requirements-%s.txt" % host_type() )
    if not os.path.isfile( fn ):
        print("warning: missing %s" % fn)
        return
    
    get_exes( )
    tmp = PIP_EXE[:]
    tmp.extend(["install", "-r", fn])
    print("tmp=%s" % tmp)
    execute( tmp )

def create_venv( ):
    execute( [PYTHON3_EXE, "-m", "venv", VENV_DIR] )
    # these have changed update them
    get_exes()

def get_pythonpath():
    global PYTHONPATH
    # default
    new_path=[MODULES_DIR]
    # Is there an existing one?
    if "PYTHONPATH" in os.environ:
        # get the old one and split to an array
        old_path = os.environ["PYTHONPATH"].split(':')
        # Do not add duplicates
        if MODULES_DIR not in old_path:
            # Ok we need to add this dir
            new_path = [ MODULES_DIR, *old_path ]
    sep=':' # MAC & LINUX
    if host_type() == 'Windows':
        sep = ';' # why is this so hard!
    PYTHONPATH=sep.join(new_path)
    verbose_print(1,"PYTHONPATH=%s" % PYTHONPATH )

def create_lostarm_python_sh():
    get_exes()
    get_pythonpath()
    text = ""
    modified = False
    if os.path.isfile(LOSTARM_PYTHON_SETTINGS_SH):
        with open( LOSTARM_PYTHON_SETTINGS_SH, "rt" ) as f:
            text = f.read()
    # if needed, add these
    if 'PYTHONPATH' not in text:
        text = text + "\nexport PYTHONPATH=%s\n" % PYTHONPATH
        modified = True
    if 'LOSTARM_PYTHON3_EXE' not in text:
        text = text + "\nexport LOSTARM_PYTHON3_EXE=%s\n" % PYTHON3_EXE
        modified = True
    # future: we add more here?
    if modified:
        with open(LOSTARM_PYTHON_SETTINGS_SH, "wt" ) as f:
            f.write( text )
        verbose_print(1,"Updated: %s" % LOSTARM_PYTHON_SETTINGS_SH)
        verbose_print(1, text )
        
        
def update_activate():
    txt = ""
    modified = False
    verbose_print(1,"Update: %s" % ACTIVATE_SH)
    if os.path.isfile( ACTIVATE_SH ):
        with open( ACTIVATE_SH, "rt" ) as f:
            txt = f.read()
    if LOSTARM_PYTHON_SETTINGS_SH not in txt:
        txt = txt + "\nsource %s\n" % LOSTARM_PYTHON_SETTINGS_SH
        modified = True
    if modified:
        with open( ACTIVATE_SH, "wt" ) as f:
            f.write( txt )
        verbose_print(1,"Updated: %s" % ACTIVATE_SH )
        verbose_print(1, txt )

def update_vscode_launch():
    get_exes()
    fn_launch = VSCODE_LAUNCH_JSON
    mod = False
    if os.path.isfile( fn_launch ):
        txt = ""
        with open( fn_launch, "rt" ) as f:
            txt = f.read()
        data = json.loads( txt )
    else:
        mod = True
        data = {}
    ok=False
    if 'version' in data:
        tmp=data['version']
        if tmp == "0.2.0":
            ok=True
    else:
        data['version']="0.2.0"
        ok=True
    if not ok:
        verbose_print(0,"%s: version is not 0.2.0" % fn_launch )
        sys.exit(1)
    la_cfg = dict()
    our_name="LOSTARM: Python"
    la_cfg['name'] = our_name
    la_cfg['type'] = "debugpy"
    la_cfg['request']="launch"
    la_cfg['program']="${file}"
    la_cfg['console']="integratedTerminal"
    la_cfg['python'] = PYTHON3_EXE
    # This lets us debug things in the python/modules directory.
    la_cfg['justMyCode']=False
    # No we do not do this
    #  la_cfg['cwd']=os.path.dirname( VSCODE_DIR )
    la_cfg['env'] = dict()
    la_cfg['env']['PYTHONPATH'] = PYTHONPATH
    la_cfg['env']['LOSTARM_PYTHON3_EXE']=PYTHON3_EXE
    
    # Make sure we have something to iterate over
    if 'configurations' not in data:
        data['configurations'] = []
        mod = True
    # See if it already exists.
    found = False
    for tmp in data['configurations']:
        if tmp['name'] == la_cfg['name']:
            # duplicate
            found = True
            break
        
    if found:
        new_configs = data['configurations']
    else:
        mod = True
        configs=[la_cfg]
        # put ours in front
        configs.extend( data['configurations'] )
    
    if mod:
        data['configurations'] = configs
        verbose_print(1,"Update: %s" % fn_launch)
        with open( fn_launch, "wt" ) as f:
            f.write( json.dumps( data, indent=4 ) )

def add_spelling_words( mod : bool, data : dict) -> tuple[bool,dict]:
    """
    We have our list of 'spelling words' in the python directory
    we wish to seed these into vscode cSpell.words
    """
    # get existing word list that vscode knows about
    key='cSpell.words'
    if key not in data:
        data[key]=[]
        mod = True
    existing = data.get(key)
    assert( isinstance( existing,list) )
    # Get our list
    fn=os.path.join(os.path.dirname(os.path.abspath(__file__)),"spelling.txt")
    our_words = []
    with open(fn,"rt") as f:
        our_words = f.readlines()
    # if our word is not in the existing list, add our word
    for this_word in our_words:
        # remove leading/trailing whitespace
        this_word = this_word.strip()
        # Ignore blank lines
        if len(this_word)==0:
            continue
        # ignore comments
        if this_word[0] == '#':
            continue
        # ok it is a word check it.
        if this_word not in existing:
            mod = True
            existing.append(this_word)
    if mod:
        data[key] = existing
    return mod, data

def update_dict( mod : bool, data : dict, key : str, val : (str|list)) -> tuple[bool,dict]:
    """
    If key is not in the data dict, add it
    if value does not match, change it
    Return (modified, data )
    """
    if key not in data:
        mod = True
        data[key] = val
    elif isinstance( val, str ):
        if data[key] != val:
            mod = True
            data[key]=val
    elif isinstance( val, list ):
        mod = True
        existing = data[key]
        if isinstance( existing, str ):
            existing = [ existing ]
        assert( isinstance( existing, list ))
        combined = dict()
        for this_entry in val:
            combined[this_entry] = 1
        for this_entry in existing:
            combined[this_entry] = 1
        data[key] = list( combined.keys() )
    return (mod,data)

def add_python_to_settings():
    
    fn = VSCODE_SETTINGS_JSON
    modified = False
    # attempt to modify the existing.
    if os.path.isfile( fn ):
        txt = None
        with open(fn,"rt") as f:
            txt = f.read()
        verbose_print(1,"Reading: %s\n%s\n" % (fn,txt))
        data = json.loads( txt )
        assert( isinstance( data, dict ))
    else:
        # does not exist, so create
        modified = True
        data = dict()
    assert( isinstance(data,dict))
    key="python.defaultInterpreterPath"
    (modified, data) = update_dict( modified, data, key, PYTHON3_EXE )
    key = "python.linting.pylintEnabled"
    (modified, data) = update_dict( modified, data,key, True )
    key = 'python.linting.enabled'
    (modified, data) = update_dict( modified,data,key,True)
    key = 'python.pythonPath'
    (modified, data) = update_dict( modified, data,key,PYTHON3_EXE)
    key = "python.analysis.extraPaths"
    (modified, data) = update_dict( modified, data, key, [ MODULES_DIR ])
    key =   "python.analysis.typeCheckingMode"
    (modified, data) = update_dict( modified, data, key, "strict" )

    (modified, data) = add_spelling_words( modified, data )
    dname = os.path.dirname( fn )
    if not os.path.isdir(dname):
        modified = True
        os.makedirs(dname)
    if modified:
        with open(fn,"wt" ) as f:
            json.dump( data, f, indent=4 )
        verbose_print(1,"Updated: %s" % fn )

def main( project_root_dir ):
    verbose_print(1,"ROOT=%s" % project_root_dir)
    set_proj_root_dir( project_root_dir )
    get_exes()
    if not os.path.isdir( VENV_DIR ):
        create_venv()
        run_requirements()
    get_pythonpath()
    create_lostarm_python_sh()
    update_activate()
    add_python_to_settings()
    update_activate()
    update_vscode_launch()

def usage():
    print("usage: %s [-v] PROJECTROOTDIR\n" % sys.argv[0])
    sys.exit(1)
    
    
if __name__ == '__main__':
    dn=None
    for tmp in sys.argv[1:]:
        if tmp == '-v':
            VERBOSE=VERBOSE +1
            continue
        if dn is not None:
            print("Duplicate PROJECTROOTDIR")
            usage()
        dn = os.path.abspath(tmp)

    if dn is None:
        usage()
    main( dn )
