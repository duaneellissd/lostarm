import sys

_unit_test_mode = False

def set_unit_test_mode():
    """
    See UnitTestException
    """
    global _unit_test_mode
    _unit_test_mode = True

class UnitTestException(Exception):
    """
    The normal action to a fatal syntax error is to exit the app.
    That makes it really hard to write unit-tests for a parser.

    So - have this instead
    If UnitTestMode is set, then we raise this exception.
    In the unit test - we catch this exception.
    """
    def __init__(self, msg ) -> None:
        Exception.__init__(self,msg)


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
        self.verbosity: int = 0
        self.filename: str = ""
        self.lineno: int = 0

    def warning(self, msg):
        self.verbose_print(0, msg)

    def fatal_set_lineno(self, lineno: int):
        self.lineno = lineno

    def fatal_set_filename(self, filename: str, lineno: int):
        """

        If we are going to die, it is more helpful to the user if the
        error message included a filename and line number that they
        can click within their IDE.

        This is contrary to normal Pythonic way:
            Normal Python is to just throw and exception
            IMHO that is nasty Python Vomit and not helpful.

        Instead, we want IDE clickable error messages that are friendly.

        They user may have a typo or other logic error in their data
        files being processed or parsed. Like any C compiler, it should
        not "vomit" a compiler seg fault or execption. A good compiler gives
        a good (IDE clickable) error message.

        If this tool generates VOMIT I consider that a bug in the tool.
        The user should report such an issue as a bug.
        """
        if filename is None:
            filename = ""
        self.filename = filename
        self.lineno = lineno

    def set_verbosity(self, verbosity: int):
        self.verbosity = verbosity

    def inc_verbosity(self) -> None:
        self.set_verbosity(self.verbosity + 1)

    def verbose_print(self, level, msg):
        if (level == 0) or (self.verbosity > level):
            sys.stdout.write(msg)
            if msg[-1] != '\n':
                sys.stdout.write('\n')
            sys.stdout.flush()

    def unit_test_fatal(self, msg : str ) -> None:
        if _unit_test_mode:
            raise UnitTestException( msg )
        if is_debugger_present():
            # Raise in the debugger do not exit.
            # makes it easier to debug things.
            # PYCHARM captures the error nicely
            # You can explore the stack backtrace in the debugger.
            raise Exception(msg)
        else:
            # Not in the debugger, print and exit..
            self.verbose_print(0, msg)
        sys.exit(1)


    def fatal(self, msg: str) -> None:
        """
        We are going to die, give a user a helpful message.
        and if it is related to a file, give the filename and lineno too.
        The goal is an error message should be clickable in the users IDE
        """
        fn = self.filename
        if isinstance(fn, str):
            use_fn = True
        else:
            use_fn = False
        if self.lineno is None:
            use_fn = False
            ln = 0
        else:
            ln = int(self.lineno)
        if use_fn:
            use_fn = len(fn) > 0
        if use_fn:
            self.fatal_here(self.filename, ln, msg)
        else:
            self.verbose_print(0, msg)
        if is_debugger_present():
            raise Exception("Bang - fatal")
        sys.exit(1)

    def fatal_here(self, filename: str, lineno: int, msg: str) -> None:
        msg = "%s:%d Fatal: %s" % (filename, lineno, msg)
        self.unit_test_fatal(msg)


_debug_output = _DebugOutput()

class VerbosePrint(object):
    def __init__(self):
        # We use the singleton.
        self._debug_out = _debug_output
    def set_verbosity(self, verbosity: int)->None:
        self._debug_out.set_verbosity(verbosity)
    def verbose_print(self, level : int, msg: str )->None:
        self._debug_out.verbose_print(level, msg)
    def fatal_or_raise(self, exception : Exception ) -> None:
        self._debug_out.fatal_or_raise( exception )
    def fatal(self, msg : str)->None:
        self._debug_out.fatal(msg)
    def fatal_set_filename(self, filename : str, lineno : int ):
        self._debug_out.fatal_set_filename( filename, lineno )
    def fatal_set_lineno(self, lineno : int ):
        self._debug_out.fatal_set_lineno( lineno )
    def fatal_here(self, filename : str, lineno : int, msg : str)->None:
        self._debug_out.fatal_here(filename,lineno,msg)
    def warning(self, msg: str )->None:
        self._debug_out.warning(msg)
