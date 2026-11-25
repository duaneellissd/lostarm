import os
import sys
import platform

PROJ_PYTHON_EXE=""
PYTHONPATH=""

def activate_sh( input_lines : list[str] ) -> list[str]:
    """
    This updates the 'activate' unix shell(bash?) script.
    It is used for windows git-bash and linux and darwin(macos)
    """
    # copy over the input lines.
    output_lines = input_lines[:]
    # All we do is add some comments and export two variables.
    output_lines.append("#")
    output_lines.append("# This was added by: %s" % os.path.abspath(__file__) )
    output_lines.append("#")

    if '"' in PROJ_PYTHON_EXE:
        print("PROJ_PYTHON_EXE=%s" % PROJ_PYTHON_EXE )
        print("Why does this contain quotes?")
        sys.exit(1)

    if '"' in PYTHONPATH:
        print("PYTHON=%s" % PYTHONPATH )
        print("Why does this contain quotes?")
        sys.exit(1)

    # We always export these QUOTED in the script.
    output_lines.append('export PROJ_PYTHON_EXE="%s"' % PROJ_PYTHON_EXE )
    output_lines.append('export PYTHONPATH="%s"'      % PYTHONPATH )
    return output_lines

def activate_bat(input_lines : list[str]) -> list[str]:
    """
    This updates the lines in the activate.bat file a standard windows batch file.
    """
    # copy over the input lines.
    output_lines = input_lines[:]
    # for a windows batch file we just add a few comments
    # and set the two variables.
    output_lines.append("rem")
    output_lines.append("rem This was added by: %s" % os.path.abspath(__file__) )
    output_lines.append("rem ")
    #
    # Windows has a NASTY problem with spaces in pathnames.
    # The classic example is this case is: "C:\Program Files\Python"
    # We require this to be in double quotes already.
    #
    # We do not add quotes here.
    #
    output_lines.append('set PROJ_PYTHON_EXE=%s' % PROJ_PYTHON_EXE)
    output_lines.append('set PYTHONPATH=%s'      % PYTHONPATH )
    # return the updated lines.
    return output_lines

def activate_ps1(input_lines : list[str] ) -> list[str]:
    """
    This updates the lines of a power shell activation script.
    """
    # newer versions of "activate.ps1" have a digital signature block.
    # Older versions of "activate.ps1" does not have a signature block.
    #
    # Details here:
    # https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_signing?view=powershell-7.6
    #
    # We are modifying the activation script so we are going to break
    # that digital signature. thus we remove the "# SIG" block.
    #
    # We have little choice here because our Python modules are not "installed"
    #
    # WHY? They are just modules within this GIT REPO...
    # And thus by default python and other tools will not find them.
    # To make these "findable" we must set the PYTHONPATH
    # And for our own purposes we must re-point PROJ_PYTHON_EXE to the VENV.
    #
    # We cannot do this in our own wrapper becuase other tools (ie: VsCODE)
    # Will not execute our wrapper, and will instead re-auto-execute
    # the powershell activate.ps1 script canceling anything we do in our wrapper
    #
    # the signature block is very simple to parse.
    # the block begins/ends with a line that starts with '# SIG'
    state = 0 # before # SIG
    # state=1 at first # SIG
    # state=2 ignoring the sig block content.
    # state=3 at second # SIG
    # state=4 after the second # SIG.
    # any other state is invalid.
    output_lines=[]
    for ln,tmp in enumerate( input_lines ):
        if tmp.startswith('# SIG'):
            # Advance to the next state.
            state = state + 1
        if state == 0:
            # before first # SIG.
            output_lines.append( tmp )
            continue
        if state == 1:
            # at first "# SIG" advance to the next state.
            output_lines.append("# Note SIG block was removed by:")
            output_lines.append("# This script: %s" % os.path.abspath(__file__) )
            state = state + 1
            continue
        
        if state == 2:
            # ignoring the # SIG block.
            continue
        if state == 3:
            # at second "# SIG"
            state = state + 1
            continue
        if state == 4:
            output_lines.append(tmp)
            continue
        # if we are not in states 0...4 something is wrong with our logic.           
        raise Exception("%s:%d: Illegal # SIG parse state(not-end) %d" % (filename,ln,state))
        sys.exit(1)
    # done parsing.
    if state != 4:
        # We should have found the # SIG marker 2 times.
        # and should have ended up in state 4.
        raise Exception("%s:%d: Illegal # SIG parse state(end): %d" % (filename,ln,state))

    output_lines.append("#")
    output_lines.append("# This was added by: %s" % os.path.abspath(__file__) )
    output_lines.append("#")
    output_lines.append('$ENV:PROJ_PYTHON_EXE="%s"' % PROJ_PYTHON_EXE )
    output_lines.append('$ENV:PYTHONPATH="%s"' % PYTHONPATH )
    return output_lines

def update_script( filename : str, handler : callable ) -> None:
    """
    Given a script - read lines of the script.
    Call the script-type-handler, which will modify/update the lines.
    Then re-write the script with the updated lines.
    """
    if not os.path.isfile( filename ):
        print("%s: No such file" % filename )
        sys.exit(1)
    # read the lines of the script
    with open( filename, "rt" ) as f:
        lines = f.readlines()
    # Call the file type handler.
    output_lines = handler( filename, input_lines )
    # Rewrite the script.
    with open( filename, "wt" ) as f:
        for tmp in output_lines:
            tmp = tmp.lstrip()
            f.write("%s\n" % tmp )
        # Alway end with an extra blank line.
        f.write("\n")
    # make it globally read/write/executable.
    os.chmod( filename, 0o777 )
 
def update_venv_dir( dirname ):
    """
    Inside the 'dirname' (aka: the venv) there are various activation scripts.
    The job here is to update the various "activate" scripts
    So that they point to *OUR* PYTHON PATH
    And reset our PROJ_PYTHON_EXE to come from the VENV.
    """
    global PROJ_PYTHON_EXE
    global PYTHONPATH

    PROJ_PYTHON_EXE = os.environ.get( "PROJ_PYTHON_EXE" )
    if PROJ_PYTHON_EXE is None:
        print("Variable: PROJ_PYTHON_EXE does not exist, it is required")
        sys.exit(1)
    
    PYTHONPATH = os.environ.get( "PYTHONPATH" )
    if PYTHONPATH is None:
        print("Variable: PYTHONPATH is not defined, it is required")
        sys.exit(1)
                        
    pt = platform.system()
    if pt == 'Windows':
        update_script( os.path.join( dirname, "Scripts", "activate.bat" ), activate_bat )
        update_script( os.path.join( dirname, "Scripts", "activate.ps1" ), activate_ps1 )
        # this appears to be for "windows-gitbash"
        update_script( os.path.join( dirname, "Scripts", "activate"     ), activate_sh  )
        return
    if pt in ('Linux','Darwin'):
        update_script( os.path.join( dirname, "bin", "activate"        ), activate_sh  )
        return
    print("Unknown platform: %s" % pt)
    sys.exit(1)

if __name__== '__main__':
    venv_dir = os.environ.get('PROJ_VENV_DIR')
    if venv_dir is None:
        print("FATAL: PROJ_VENV_DIR is not defined\n")
        sys.exit(1)
    update_venv_dir( venv_dir )
    sys.exit(0)
    
              
    

    
