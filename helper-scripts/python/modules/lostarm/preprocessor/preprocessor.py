"""
This file attempts to be something like a C language preprocessor for our template.
This handles:
  a) defining (discovering a macro)
  b) Playing back a macro.
  c) Include files
  d) Various @IF( expression )@, @ELSE@ and @ENDIF@

"""

import re
import os
from typing import NamedTuple
from lostarm.utils.verbose_print import VerbosePrint
from lostarm.input_file import InputFile
from lostarm.input_file import Macro, remember_macro, get_macro, all_macro_items, macro_exists
from lostarm.utils.search_path import SearchPath
from lostarm.variables import get_global_vars

class IfEntry(NamedTuple):
    filename: str
    lineno : int
    state : bool

class IfStack(VerbosePrint):
    def __init__( self, preprocessor: "PreProcessor" ) -> None:
        VerbosePrint.__init__(self)
        # Let people override this requirement.
        self.enforce_same_file = True
        self._preprocessor = preprocessor
        self._stack = []
    def _has_entry(self, filename, lineno ):
        """
        Die (fatal) if there is no stack entry
        """
        if len(self._stack) == 0:
            self.fatal_here(filename, lineno, "invalid @IF")
    def _same_filename(self, opcode: str, filename: str, lineno: int ) -> None:
        """
        For some things, @IF@, @ELSE@ and @ENDIF@ we expect these
        to be in the same file as the @NAME@ element.
        Meaning the @IF@ and @ELSE@ and @ENDIF@ should be in the same filename
        Otherwise things get sort of wacky.

        This includes by extension @ELSE_IF@ type statements.
        """
        # only enforce this if it is enabled.
        if not self.enforce_same_file:
            return
        # we are called due to an @ELSE@ or @ENDIF@
        # So obviously we should be inside an if,
        # so we MUST have a stack entry.
        if len( self._stack) == 0:
            self.fatal_here( filename,lineno, "Missing opening @IF@" )
        # Get the top of the stack
        tos = self._stack[-1]
        if tos.filename == filename:
            # ALL IS WELL.
            return
        # Give human a reasonably clickable IDE friendly error
        # We do not want to generate PYTHON VOMIT here.
        self.verbose_print(0, "%s:%d: ERROR: IF/ELSE was here" % (tos.filename, tos.lineno))
        self.fatal_here( filename,lineno, "ELSE/ENDIF is not in same file")

    def open_if(self, filename : str, lineno : int, state: bool, is_else_if : bool ):
        """
        The preprocessor has found an IF of some sort.
        We need to open(push) an if entry onto the sack.
        For @ELSEIF@ we must modify/update the top of the stack.
        """
        if is_else_if:
            # Syntactically we require these to be in the same file.
            self._same_filename( "IF", filename, lineno)
            # get TOP OF STACK, tos
            tos = self._stack[-1]
            tos.filename = filename
            tos.lineno = lineno
            tos.state = state
            # replace top of stack.
            self._stack[-1] = tos
        else:
            # Not an ELSEIF so we push onto the stack.
            tos = IfEntry( filename=filename, lineno=lineno, state=state)
            self._stack.append(tos)

    def handle_else(self, filename : str, lineno : int ):
        """
        The Preprocessor has found an else statement. handle it.
        """
        self._same_filename("ELSE", filename, lineno )
        # Get TOP OF STACK, tos
        tos = self._stack[-1]
        tos.filename = filename
        tos.lineno = lineno
        # Flip the state.
        tos.state = not tos.state
        # replace top of stack.
        self._stack[-1] = tos

    def handle_endif(self, filename : str, lineno : int ):
        """
        The preprocessor has found an @ENDIF@ pop it off the stack
        """
        self._same_filename( "ENDIF", filename, lineno )
        self._stack.pop()


# macros begin with @MACRO_BEGIN(name)@ and end with @MACRO_END(name)@
# these regex are what we use to find the macro begin/end.
# NOTE: LHS = Left Hand Side, RHS = Right Hand Side
re_macro_begin = re.compile( r"^(?P<LHS>.*)@MACRO_BEGIN[(][ \t]*(?P<name>[A-Za-z_][A-Za-z_0-9]*)[ \t]*[)]@(?P<RHS>.*)$" )
re_macro_end = re.compile( r"^(?P<LHS>.*)@MACRO_END[(][ \t]*(?P<name>[A-Za-z_][A-Za-z_0-9]*)[ \t]*[)]@(?P<RHS>.*)$")


class PreProcessor(VerbosePrint):
    """
    This is a PULL type PreProcessor.
    A PULL parser calls a function to get the next line of text from the input.
    A PUSH parser is called with a line handle the line of text from the input.

    This preprocessor handles a number of other features.
        @IF(expression)@, @ELSE@, and @ENDIF@
        the "expression" is very limited.
    In addition, these other @IF@ like things are supported.
        @IF_DEFINED( varname )@
        @IF_NOT_DEFINED( varname )@
        @ELSE_IF_DEFINED(varname)@
        @ELSE_IF_NOT_DEFINED(varname)

    Macros can also be created like this:
        @MACRO_BEGIN(name)@
        ... lines of text ...
        @MACRO_END(name)@

    NOTE: The "macro-name" must be unique.

    When generating a "Makefile" - the @MACRO@ is used
    to generate rules for various source files.
    """
    def __init__(self):
        VerbosePrint.__init__(self)
        self._unget_line_buf = None
        self._include_stack: list[InputFile] = []
        self._shell_variables = get_global_vars()
        """
        Should we support ${VARS} in @INCLUDE statements?
        """
        self.support_variables = True
        """
        Should we support @INCLUDE( "filename" )@
        """
        self.support_include = True
        """
        Where do we search for @INCLUDE( "filenames" )@
        """
        self._search_path : SearchPath = SearchPath()
        """
        Does the preprocessor support @IF/ELSE/ENDIF@?
        """
        self.support_if_else_endif = True
        """
        Should we support @MACRO_BEGIN(name)@
        """
        self.support_macros = True
        """
        Should macros be of a limited length?
        Consider the case where we find @MACRO_BEGIN()@
        But we never find @MACRO_END()@ due to a typo/syntax error?
        If this is -1, the size is unlimited.
        """
        self.reasonable_macro_length = 200

    def resolve_text(self, text : str ) -> str:
        """
        This adds support for ${variables}.
        """
        if self.support_variables:
            # call the resolver.
            tmp = self._shell_variables.resolve_text(text)
        else:
            # No support, just return the text we got.
            tmp = text
        return tmp

    def syntax_error(self, msg : str ) -> None:
        """
        We are dead, and cannot parse any more due to a syntax error
        """
        self.fatal_here( self.cur_filename(), self.cur_lineno(), "Syntax Error: %s" % msg )

    def _unget_line(self, s : str ):
        """
        We allow a single UNGET (Makes parsing easier)
        """
        assert( self._unget_line_buf is None )
        self._unget_line_buf = s

    def cur_filename(self) -> str:
        entry = self._include_stack[-1]
        return entry.get_filename()
    def cur_lineno(self):
        entry = self._include_stack[-1]
        return entry.lineno

    def add_search_dir(self, s: str) -> None:
        """
        Adds a search directory for include like operations.
        """
        if not os.path.isdir(s):
            self.fatal("%s: Not a directory" % s )
        self._search_path.add_search_dir(s)

    def dumpStack(self):
        """
        We are going to die, print the include stack like a compiler does
        ie: foo.c:50: included from here
        ie: bar.c:20: included from here
        """
        for n, entry in enumerate(self._include_stack):
            fn = entry.get_filename()
            if entry.is_macro == 'macro':
                msg = "%s:%d: Macro: %s -> from here" % (fn, entry.lineno, entry.macro_name)
            else:
                msg = "%s:%d -> from here" % (fn, entry.lineno)
            self.verbose_print(0, msg )

    def findFile(self, filename: str) -> str:
        """
        Given a filename try to find it.
        if the filename is an abspath, just use it.
        If not abspath, then search relative to
        """
        result = self._search_path.find_relative_to( filename, self.cur_filename() )
        return result

    def invoke_macro(self, name : str):
        """
        A macro has a name and appears and acts like an include file.
        """
        if not macro_exists(name):
            self.verbose_print( 0, "no such macro: %s" % name )
            self.verbose_print( 0, "Available macros are:")
            for n, macro in all_macro_items():
                self.verbose_print( 0, "%s -> %s:%d" % (n, macro.filename, macro.lineno) )
            self.fatal("no such macro: %s" % name )
        else:
            the_macro = get_macro(name)
            # convert the macro to an input file.
            fake_file : InputFile = InputFile.from_macro( the_macro )
            self._include_stack.append( fake_file )
    def open(self, filename : str ) -> None:
        """
        Opens - effectively pushes into the include stack.
        """
        inp_filename = InputFile.from_file( filename )
        self._include_stack.append(inp_filename)
        if len(self._include_stack) > 30:
            self.dumpStack()
            self.fatal("Include stack overflow > 30 items?")
        self._reset_filename_lineno()

    def _reset_filename_lineno(self) -> None:
        """
        When we open a new file,or pop the include stack.
        We need to update the filename and line number
        used by the verbose.fatal() call.

        This does that for us.
        """
        tos = self._include_stack[-1]
        self.fatal_set_filename( tos.get_filename(), tos.lineno )

    def pop(self):
        """
        We have reached the end of an include file
        We need to pop the include stack and resume the previous file.
        """
        assert (len(self._include_stack) > 0)
        self._include_stack.pop()
        if len(self._include_stack) > 0:
            self._reset_filename_lineno()
        else:
            # We have closed the very first (initial) fle
            pass

    def is_eof(self):
        """
        Are we at the end of all files, all input?
        """
        if self._unget_line_buf is not None:
            return False
        # Handle the pathological case.
        # you are (N) include files deep.
        # You are at the last line of each include file
        # the next read will 'pop' the entire include stack.
        for entry in self._include_stack:
            if not entry.is_eof():
                return False
        # All of these have no more
        # So we are at the very end of all input.
        return True


    def next_raw_line(self) -> str:
        """
        The RAW line is before the pre-processor.
        """
        if self._unget_line_buf is not None:
            result = self._unget_line_buf
            self._unget_line_buf = None
            return result
        txt = ""
        while True:
            if self.is_eof():
                raise EOFError()
            # Get the current file
            inp_file = self._include_stack[-1]
            if inp_file.is_eof():
                self.pop()
                continue
            else:
                txt = inp_file.next_line()
                break
        return txt

    def parent_hook(self, text : str ) -> tuple[bool,str]:
        """
        This hook exists so that the parent class of this class
        can do things as it wishes with text that is read.

        In the unit-test code for this module we use this
        to track some things

        The return is a TUPLE.
        TUPLE[0] = TRUE if the line should be skipped over.
        TUPLE[1] = The text of the line, This allows the hook to modify the text
        """
        # the default implementation does nothing
        return False,text



    def consume_macro(self, opening_line : str ) -> None:
        m = re_macro_begin.match( opening_line )
        if m is None:
            self.syntax_error("invalid macro begin (basic regex)")
        tmp = m['LHS'].strip()
        if tmp != "":
            self.syntax_error("Invalid macro begin (LHS=%s)" % tmp)
        tmp = m['RHS'].strip()
        if tmp != "":
            self.syntax_error("Invalid macro begin (RHS=%s)" % tmp)
        start_name = m['name']
        start_fn = self.cur_filename()
        start_ln = self.cur_lineno()
        lines = []

        max_lines = self.reasonable_macro_length
        while True:
            raw_line = self.next_raw_line()
            if '@MACRO_END' in raw_line:
                break
            # catch goofy syntax errors with @MACRO statements.
            if '@MACRO' in raw_line:
                self.verbose_print(0,"%s:%d: Macro(%s) Opened here" % (start_fn,start_ln,start_name) )
                self.syntax_error("@MACRO within a macro is not supported")
            lines.append(raw_line)
            if max_lines < 0:
                # No limit
                continue
            if len(lines) < max_lines:
                # not to many yet.
                continue
            # This macro is rather huge something is probably wrong. Stop.
            self.verbose_print(0,"%s:%d: ERROR: Macro(%s) begins" % (start_fn,start_ln,start_name) )
            self.verbose_print(0,"%s:%d: ERROR: Macro(%s) is exceeded %d lines" % ( self.cur_filename(), self.cur_lineno(), start_name, max_lines))
            self.fatal("Sorry cannot continue")
        # is the MACRO_END() syntactically correct?
        m = re_macro_end.match(raw_line.strip())
        if m is None:
            self.syntax_error("Invalid @MACRO_END(name)@- no match")
        tmp = m['LHS'].strip()
        if tmp != "": # LHS should be blank.
            self.syntax_error("Invalid @MACRO_END(name)@- LHS")
        tmp = m['RHS'].strip()
        if tmp != "": # RHS should be blank.
            self.syntax_error("Invalid @MACRO_END(name)@- RHS")
        tmp = m['name']
        end_name = str(tmp) # shut up pylance.
        end_fn = self.cur_filename()
        end_ln = self.cur_lineno()
        # Macros must start/end in the SAME file.
        if (start_fn != end_fn) or (start_name != end_name):
            self.verbose_print(0, "%s:%d: ERROR: Macro(%s) begins" % (start_fn, start_ln, start_name))
            self.verbose_print( 0, "%s:%d: ERROR: Macro(%s) end - filename or macro name do not match" % (end_fn, end_ln, end_name))
            self.fatal_here( tmp, self.cur_lineno(),"Macro must end in the same file" )
        # We have captured the macro remember it.
        remember_macro( start_name, start_fn, start_ln, lines )

    def _is_if_else_endif(self, text ) -> bool:
        text = text.lstrip()
        if text.startswith( '@IF'):
            self.handle_if(text,False)
            return True
        if text.startswith( '@ELSE' ):
            self._handle_else(text)
            return True
        if text.startswith('@ENDIF@'):
            self._handle_endif(text)
            return True
        # None of the above
        return False

    def _quoted_string(self, prefix, text ):
        """
        We have an @INClUDE( "quoted-filename" )@
        extract the quoted filename.
        """
        # We want a single quote at start/end, not doulbes, etc.
        # so block that here.
        if ('""' in text) or ("''" in text):
            self.syntax_error("quote syntax, expected: %s or %s" % ('"foo"', "'foo'"))
        # Remove the @INCLUDE( part
        text = text[ len(prefix): ]
        # Remove leading/trailing white space..
        text = text.strip()
        # The directive must end with an )@ nothing else, ie: no comments at end of line.
        if not text.endswith(")@"):
            self.syntax_error("Closing )@")
        # remove the )@ at the end.
        # and remove trailing whitespace after filename and before )@
        text = text[:-2].strip()
        # TEXT is generally our "filename"
        # it may be quoted, or maybe it is not, we do not know.
        if len(text) >= 3:
            # We must have the 2 quotes + 1 char to be a quoted filename
            # check to see if it starts with a quote.
            if text[0] in ("'",'"'):
                # Does opening/closing match?
                if text[0] != text[-1]:
                    # It does not... so die.
                    self.syntax_error("Mismatched quotes in @INCLUDE")
                # remove the quotes and we are done.
                text = text[1:-1]
                # expand ${VARS}
                result = self.resolve_text( text )
                return result
        # otherwise it is not a quote string.
        # there should be no quotes inside the string.
        # This happens if there are typos in the string.
        if ('"' in text) or ("'" in text):
            self.syntax_error("bad quotes in @INCLUDE")
        # return the result we found
        text = text.strip()
        # remove ${variables}
        text = self.resolve_text( text )
        return text

    def _handle_include(self, text : str ) -> None:
        """
        This handles @INCLUDE( "quoted-filename" )@

        One can also add a search directory via:

        This also handles @INCLUDE_ADD_SEARCH_DIR( "path-to-some-dir" )@
        """
        # Remove leading/trailing whitespace.
        text = text.strip()
        if text.startswith( '@INCLUDE(' ):
            # This also handles ${variables}
            filename = self._quoted_string( "@INCLUDE(", text )
            filename = self.findFile( filename )
            self.open( filename )
            # Success.
            return
        # the other @IMN
        if text.startswith( '@INCLUDE_ADD_SEARCH_DIR(' ):
            dirname = self._quoted_string( "@INCLUDE_ADD_SEARCH_DIR(", text )
            if os.path.isabs(dirname):
                the_dir = dirname
            else:
                # Then make it relative to the current filename
                this_dir = os.path.dirname( self.cur_filename() )
                the_dir = os.path.join( this_dir, dirname )
                if '..' in the_dir:
                    the_dir = os.path.realpath( the_dir )
            if not os.path.isdir(the_dir):
                self.fatal("%s: @INCLUDE_ADD_SEARCH_DIR()@ Not a directory" % the_dir)
            self.add_search_dir( the_dir )
            # Success.
            return
        self.syntax_error("@INCLUDE syntax error, not recognized")

    def next_preprocessed_line(self) -> str:
        # Read the next preprocessed line
        while True:
            orig_text = self.next_raw_line()
            # Let the parent do something?
            (skip,tmp) = self.parent_hook(orig_text)
            if skip:
                continue
            assert( isinstance( tmp, str ) )

            # If we are supporting macros.
            if self.support_macros:
                if '@MACRO' in tmp:
                    self.consume_macro(tmp)
                    continue
            # If we are support if/else/endif
            if self.support_if_else_endif:
                if self._is_if_else_endif(tmp):
                    continue
            if self.support_include:
                if '@INCLUDE' in tmp:
                    self._handle_include( tmp )
                    continue
            break
        # We have a line!
        return orig_text

