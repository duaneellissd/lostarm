"""
ALl debug output and fatal things go through the _DebugOutput class.
Note:
    1) This is class is effectively a singleton.
    2) Below we have a global: "debug_output"
    3) Other things use VerbosePrint() which uses the single common _DebugOutput class.
"""
import os
import sys
import json

__ALL__ = ["VerbosePrint", "safe_json_load", "safe_json_save", "is_debugger_present" ]

def is_debugger_present():
    """
    This is a tool, so if a parse or logic error exists in the
    users (our victims) data file we are parsing occurs.

    It is bad practice to produce a python callstack (aka: Python Vomit)
    it is better to produce a usable, IDE friendly clickable error message

    By way of an example: When you have a syntax error in your C code
    Does the compiler give you a nice error message?
    Or does the compiler print a stack dump as the error message?

    If a user is running this from the command line, we probably
    want the error message.  But sometimes the developer of this tool
    is running the tool inside a python debugger.  An exception
    might be a better choice - so this helps make that decision.
    """
    tmp = sys.gettrace()
    if tmp is not None:
        return True
    # VS Code and others sometimes work very differently.
    # GRRR!
    if 'debugpy' in sys.modules:
        import debugpy as tmp
        tmp2 = tmp.is_client_connected()
        return tmp2
    else:
        return False


class _DebugOutput(object):
    """
    ALl debug output and fatal things go through this class.
    Note:
        1) This is class is effectively a singleton.
        2) Below we have a global: "debug_output"
        3) Other things use VerbosePrint() which uses the single common _DebugOutput class.
    """
    def __init__(self):
        self.verbosity : int = 0
        self.where_stack = []
        self.filename : str = ""
        self.lineno : int = 0

    def fatal_where_set(self, filename : str, lineno : int):
        """
        If we are going to die, it is more helpful to the user if the
        error message included a filename and line number that they
        can click within their IDE.

        This is contrary to normal Pythonic way:
            Normal Python is to just throw and exception and be done with it.
        We do not do that for a reason
            This is a tool the user is using.
        They user may have a typo in their data files being processed.
        Like any C compiler, it should not "vomit" a compiler seg fault.
        A good compiler gives a good (clickable) error message.

        That is our goal. We do not want 'python vomit'

        If this tool generates VOMIT it is bug in the tool.
        The user should report such an issue as a bug.
        """
        if filename is None:
            filename = ""
        self.filename = filename
        self.lineno = lineno

    def fatal_where_push(self, filename: str, lineno : int ) -> None:
        self.where_stack.append( (self.filename, self.lineno) )
        self.fatal_where_set( filename, lineno )
    def fatal_where_pop(self) -> None:
        assert(len(self.where_stack) > 0)
        self.filename, self.lineno = self.where_stack.pop()
    def set_verbosity(self, verbosity: int):
        self.verbosity = verbosity
    def inc_verbosity(self) -> None:
        self.set_verbosity(self.verbosity + 1)

    def verbose_print(self, level, msg ):
        if (level ==0) or (self.verbosity > level):
            sys.stdout.write(msg)
            if msg[-1] != '\n':
                sys.stdout.write('\n')
            sys.stdout.flush()


    def fatal_or_raise(self, exception : Exception)->None:
        if is_debugger_present():
            raise exception
        else:
            self.verbose_print(0, "Fatal: %s" % exception.msg )
        sys.exit(1)
    def fatal(self, msg : str ) -> None:
        """
        We are going to die, give a user a helpful message.
        and if it is related to a file, give the filename and lineno too.
        The goal is an error message should be clickable in the users IDE
        """
        use_fn = (self.filename is not None) or (self.lineno is not None)
        if use_fn:
            use_fn = len(self.filename) > 0
        if use_fn:
            self.fatal_here( self.filename, self.lineno, msg )
        else:
            self.verbose_print(0,msg)
        if is_debugger_present():
            raise Exception("Bang - fatal")
        sys.exit(1)
    def fatal_here(self, filename : str, lineno : int, msg : str ) -> None:
        if len(self.where_stack) > 0:
            for fn,ln in self.where_stack:
                self.verbose_print(0,"%s:%d: Included from here" % (fn,ln))
        self.verbose_print(0,"%s:%d Fatal: %s" % (filename, lineno, msg))
        if is_debugger_present():
            raise Exception("Bang - fatal")
        sys.exit(1)

debug_output = _DebugOutput()

class VerbosePrint(object):
    def __init__(self):
        self._debug_out = debug_output
    def set_verbosity(self, verbosity: int)->None:
        self._debug_out.set_verbosity(verbosity)
    def verbose_print(self, level : int, msg: str )->None:
        self._debug_out.verbose_print(level, msg)
    def fatal_or_raise(self, exception : Exception ) -> None:
        self._debug_out.fatal_or_raise( exception )
    def fatal(self, msg : str)->None:
        self._debug_out.fatal(msg)
    def fatal_where_push(self, filename : str, lineno : int ) -> None:
        self._debug_out.fatal_where_push(filename, lineno)
    def fatal_where_pop(self) ->None:
        self._debug_out.fatal_where_pop()
    def fatal_where_set(self, filename : str, lineno : int ):
        self._debug_out.fatal_where_push( filename, lineno )
    def fatal_here(self, filename : str, lineno : int, msg : str)->None:
        self._debug_out.fatal_here(filename,lineno,msg)

def safe_json_load( filename: str) -> dict:
    """
    Since our files are human edited, they can contain typos.
    We do not want to python.vomit on the user.
    The user deserves a much better error
    This does that for us.
    """
    tmp = VerbosePrint()
    filename = os.path.abspath(filename)
    if not os.path.isfile( filename ):
        tmp.fatal_here("%s: No such file" % filename )
    data = dict()
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
