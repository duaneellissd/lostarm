import os
import json
from lostarm.utils.verbose_print import VerbosePrint


def safe_json_load( filename: str) -> dict:
    """
    Since our files are human edited, they can contain typos.
    We do not want to python.vomit on the user.
    The user deserves a much better error
    This does that for us with IDE clickable error messages
    """
    filename = os.path.abspath(filename)
    data = dict()
    tmp = VerbosePrint()
    if not os.path.isfile( filename ):
        tmp.fatal("%s: No such file" % filename )
    tmp.verbose_print(0,"Loading: %s" % filename)
    try:
        with open( filename, "rt" ) as f:
            data = json.load( f )
    except json.decoder.JSONDecodeError as E:
        tmp.fatal_here( filename, E.lineno, E.msg )
    return data

def safe_json_save(filename : str, data: dict) -> None:
    """
    Since we expect users to edit our JSON files
    Or possibly look at them, we'll save them in
    a nice formatted style.
    """
    tmp = VerbosePrint()
    tmp.verbose_print(0,"Saving: %s" % filename)
    with open( filename, "wt" ) as f:
        json.dump( data, f, indent=4 )
