"""
The Input file is exactly two things:

Case 1 - A normal file you read from the disk drive.
Case 2 - A macro expansion.

In this template system, you might define a macro using
the @MACROBEGIN(name)@ and @MACROEND(NAME)@ This captures
a slice of lines from the input file.

When you invoke a macro that slice of lines is played back.

The use case is this:

In a makefile you might have a rule for a C file.
That rule is a bit more complex than a Make suffix rule.

Example:
    for each "c" file, execute the macro: COMPILE_c2any
    Which might invoke the macro: c2o, c2i, and c2s

"""
import os
from lostarm.input_file.macro import Macro
from lostarm.utils.verbose_print import VerbosePrint

class InputFile( VerbosePrint ):
    """
    This is an location in the include stack.
    The template system supports @INCLUDE( FILENAME )@
    This helps track the location of the read cursor.
    """
    def __init__( self ):
        VerbosePrint.__init__(self)
        self._filename : (str|None) = None
        self.lineno : int = 0
        self.lines  : list[str]  = []
        self.is_macro  : bool = False
        self.macro_name : str = ""

    def get_filename(self) -> str:
        assert( isinstance(self._filename, str) )
        return str(self._filename)

    @staticmethod
    def from_file( filename: str ) -> "InputFile":
        result = InputFile()
        result.is_macro = False
        result._filename = filename
        result.lineno = 0
        if not os.path.isfile( filename ):
            result.fatal("%s: No such file or directory" % filename )
        tmp : list[str] = []
        with open( filename, "rt") as f:
           tmp = f.readlines()
        last_line = ""
        for this_line in tmp:
            last_line = this_line
            result.lines.append(this_line)
        # complain if the last line does not end with a terminal newline.
        if not last_line.endswith('\n'):
            result.verbose_print(0,"%s:%d: Missing terminal new line" % (filename, len(result.lines)))
        return result

    @staticmethod
    def from_macro( macro : "Macro" ) -> "InputFile":
        """
        When an input macro is invoked we create a quasi-fake include file
        """
        result = InputFile()
        result.is_macro = True
        result.macro_name = macro.macro_name
        result._filename = macro.filename
        result.lineno = macro.lineno
        result.lines = macro.lines[:]
        return result

    def is_eof( self ):
        """
        Are we at the end of this file?
        """
        if len( self.lines ) == 0:
            return True
        else:
            return False

    def next_line( self ) -> str:
        """
        Read the next line from this file.
        """
        assert( not self.is_eof() )
        text = self.lines.pop(0)
        self.lineno += 1
        self.fatal_set_lineno( self.lineno )
        return text

    def comment_where_am_i(self):
        """
        Return a unix style string indication where we are located.
        Unix Like error messages have a specific format: "filename:lineno: MESSAGE"
        """
        return "%s:%d: " % ( self.get_filename(), self.lineno )