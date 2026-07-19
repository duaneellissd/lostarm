from lostarm.utils.verbose_print import VerbosePrint
from typing import NamedTuple
all_macros = dict()

def TemplateMacro( NamedTuple ):
    """
    For makefiles we often use a "macro".
    a Macro is defined as follows:
        @MACROBEGIN(name)@
        ... numerous lines of text ...
        @MACROEND(name)@
    This is that captured data.
    """
    name : str
    filename : str
    lineno : int
    lines : list[str]

def remember_macro( name: str, fn : str, ln :int , lines : list[str] ):
    old : TemplateMacro = all_macros.get(name, None)
    if old is None:
        tmp = TemplateMacro(name=name, filename=fn, lineno=ln, lines=lines[:])
        all_macros[name] = tmp
        return
    tmp = VerbosePrint()
    tmp.verbose_print(0, "%s:%d: ERROR: Duplicate macro named: %s" % (fn, ln, name))
    tmp.verbose_print(0, "%s:%d: ERROR: Old definition here" % (old.filename, old.lineno))
    tmp.fatal("Sorry, cannot continue")


