from lostarm.utils.verbose_print import VerbosePrint
from typing import NamedTuple, Any

all_macros = dict()

class Macro( NamedTuple ):
    """
    For makefiles we often use a "macro".
    a Macro is defined as follows:
        @MACROBEGIN(name)@
        ... numerous lines of text ...
        @MACROEND(name)@
    This is that captured data.
    """
    macro_name : str
    filename : str
    lineno : int
    lines : list[str]

def all_macro_items():
    return all_macros.items()

def macro_exists( name : str ) -> bool:
    return (name in all_macros)

def get_macro(name: object) -> Macro:
    """
    Lookup and get this macro by name.
    If it does not exist, it raises a KeyError
    """
    return all_macros[name]

def remember_macro( name: str, fn : str, ln :int , lines : list[str] ):
    if name in all_macros:
        old = all_macros[name]
    else:
        old = None
    if old is None:
        tmp = Macro(macro_name=name, filename=fn, lineno=ln, lines=lines[:])
        all_macros[name] = tmp
        return
    tmp = VerbosePrint()
    tmp.verbose_print(0, "%s:%d: ERROR: Duplicate macro named: %s" % (fn, ln, name))
    tmp.verbose_print(0, "%s:%d: ERROR: Old definition here" % (old.filename, old.lineno))
    tmp.fatal("Sorry, cannot continue")


