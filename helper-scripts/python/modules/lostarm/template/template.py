import re
import os
import typing
from lostarm.utils import VerbosePrint
from lostarm.variables import get_global_vars
from lostarm.input_file import InputFile
import unittest
import filecmp

re_simple_name = re.compile( r"(?P<lhs>.*)[@](?P<name>[A-Za-z_][A-Za-z0-9_]*)[@](?P<rhs>.*)$")

#
# This is a template engine.
# In general, we read a text file.
# We loop over each line in the file.
#   If the line contains @TEXT@, or @FUNC(params)@
#   Replce the @TEXT@ with the variable value of the same name.
#   Or call the specified FUNC, passing the params.
#   We replace the @FUNC(params)@ with the return value of the func.
#
# This also supports things like:
#    @IF_DEFINED(NAME)@  is this variable defined
#    @IF_NOT_DEFINED(NAME)@ is this variable not defined
#    @IF_EQUAL_NOCASE( A, B )@ // Ignores case
#    @IF_EQUAL_EXACT( A, B )@ // does not ignore case
#
#  And @ELSE_IF.. anyof the above
#  and @ENDIF@
# 


        
class If_Entry():
    def __init__( self, filename : str, lineno, parent_state, local_state ):
        self.if_filename = filename
        self.if_lineno = lineno
        self.else_filename = ""
        self.else_lineno = 0
        self.local_state = local_state
        self.parent_state = parent_state

    def set_else_loc( self, filename : str, lineno ):
        """
        An ELSE has been found, remember where it was found
        and flip the local state.
        """
        self.else_filename = filename
        self.else_lineno = lineno
        self.local_state = not self.local_state
    def is_active( self ):
        if self.parent_state and self.local_state:
            return True
        else:
            return False

class IfElseStack(VerbosePrint):
    def __init__( self ):
        VerbosePrint.__init__(self)
        self._stack = []

    def dump(self)->None:
        """
        Dump the if/else stack before a fatal error message
        """
        for entry in self._stack:
            self.verbose_print(0,"%s:%d - IF here" % (entry.if_filename, entry.if_lineno) )
            if isinstance( entry.else_filename, str ):
                self.verbose_print( 0,"%s:%d: Else here" % (entry.else_filename, entry.else_lineno) )


    def if_push( self, filename : str, lineno, state ):
        """
        We are opening a new if statement.
        """
        top = self._stack[-1]
        if_entry = If_Entry( filename, lineno, top.local_state, state )
        self._stack.append( if_entry )

    def do_else_if( self, filename : str, lineno, state ):
        """
        We have found an "elseif()" statement.
        """
        if_entry = self._stack[-1]
        if filename != if_entry.if_filename:
            self.warning("%s:%d: IF opened here" % (if_entry.if_filename, if_entry.if_lineno))
            self.warning("%s:%d: ELSE found here" % (filename,lineno))
        if_entry.if_filename = filename
        if_entry.if_lineno = lineno
        if_entry.state = state
        self._stack[-1]= if_entry

    def do_else(self, filename : str, lineno ):
        """
        We have a simple basic else statement
        """
        if_entry = self._stack[-1]
        if_entry.state = not if_entry.state
        self._stack[-1] = if_entry
    def do_endif(self, filename: str, lineno : int ) -> None:
        """
        We have found a basic endif() statement.
        """
        top = self._stack.pop()
        if filename != top.if_filename:
            self.warning("%s:%d: Warning If opened here" % (top.if_filename, top.if_lineno))
            self.warning("%s:%d: Endif found here" % (filename,lineno))
        # Let the fatal code know we changed filenames back to the old one
        # Which could be in another file!
        top = self._stack[-1]
        self.fatal_set_filename( top.if_filename, top.if_lineno )

    def is_active( self ):
        """
        Parser wants to know if the current IF block is TRUE or FALSE
        """
        if len(self._stack) == 0:
            tmp = True
        else:
            # We need to look inside.
            if_entry = self._stack[-1]
            tmp = if_entry.is_active()
        return tmp

class InputStream():
    def __init__(self):
        self._include_stack = list[Inc_Entry] = []
        self._if_else_stack = IfElseStack()

    def macro_pushback(self, filename: str, lineno: int, lines : list[str]) -> None:
        """
        When a macro is executed, it creates more template lines.
        These are pushed back into the input stream.
        ===
        What we do is create a dummy include file.
        """
        pushback = Inc_Entry()
        pushback.lines = lines[:]
        pushback.filename = filename
        pushback.lineno = lineno
        self._include_stack.append( pushback )

    def next_line(self) -> (str|None):
        """
        Return the next line we can process
        """
        while True:
            # End of file?
            if len(self._include_stack) == 0:
                # EOF.
                return None
            inc_entry = self._include_stack[-1]
            if inc_entry.is_eof():
                self._include_stack.pop()
                continue

        text = self._include_stack[-1].next_raw_line()






class OutputFile():
    def __init__(self):
        self._lines : list[str] = []
        self._fh : (typing.TextIO|None) = None
        self._filename = None
    def append_line(self, text : str ):
        self._lines.append( text )
    def open(self, filename ):
        tmp = os.path.dirname( filename )
        if not os.path.isdir(tmp):
            os.makedirs(tmp)
        self._filename = filename
        self._fh = open( self._filename, "wt" )

    def flush(self):
        self._fh.write( "\n".join(self._lines) )
        self._lines = []

    
re_ifelse = re.compile("@(ELSE|IF|ENDIF)")
    
    
class Template(VerbosePrint):
    def __init__(self):
        VerbosePrint.__init__(self)
        self._shell_vars = get_global_vars()
        self._output = OutputFile()
        self._input = InputFile()
        self.out_lines : list[str] = []
        self._include_stack : Include_Stack = Include_Stack()
        self._if_stack : IfElseStack = IfElseStack()
        self._comment_format : str = "# %s"
        self._recursion_block : int = 0

    def handle_C_COMMENT( self, text ):
        self._comment_format = "// %s"
        return ""
    
    def handle_HASH_COMMENT( self, text ):
        self._comment_format = "# %s"
        return ""

    def handle_SEMI_COMMENT( self, text ):
        self._comment_format = "; %s"
        return ""

    def handle_PS1_COMMENT(self, text ):
        # PowerShell uses hashes for 1 line comments.
        return self.handle_HASH_COMMENT(text)

    def handle_BAT_COMMENT( self, text ):
        """
        Windows batch files
        """
        self._comment_format = "REM %s"
        return ""


    def handle_INCLUDE( self, param : str ) -> None:
        """
        We have found an @INCLUDE(filename)@ of some sort.
        Push this onto our include stack.
        """
        param = param.strip()
        if not os.path.isabs(param):
            fn = self._include_stack.find( param )
        else:
            fn = param
        self._include_stack.push( fn )

    def syntax_error( self, msg ):
        """
        We are dead, we have a syntax error.
        """
        self._include_stack.dump()
        self._if_stack.dump()
        self.fatal("SYNTAX: %s" % msg )

    def process_line(self, text) -> str:
        """
        Every line - is processed by this function.
        This looks for @NAME@ or @NAME(params)@ and
        provides replacements
        """
        # bad things never happen with recursive macros do they?
        self._recursion_block += 1
        if self._recursion_block > 50:
            self.fatal("Hmm process_line() is 50 levels deep is this expected?")
        result = self._process_line_internal( text )
        self._recursion_block -= 1
        return result

    def _if_push( self, state ):
        """
        We have encountered some type of "@IF" statement
        """
        inc_entry = self._include_stack[-1]
        if_entry = IfElseEntry(inc_entry.filename, inc_entry.cur_lineno, "",0,state )
        self._if_else_stack.append( if_entry )
        
    def _elif_set( self, new_state ):
        """
        WE have found an @ELSE_IF of some type.
        """
        inc_entry = self._include_stack[-1]
        if_entry = self._if_else_stack[-1]
        if_entry.state = new_state
        if_entry.if_fileanme = inc_entry.filename
        if_entry.if_lineno = inc_entry.lineno
        self._if_else_stack[-1] = if_entry
        
    def _else_toggle( self ):
        """
        We have found a plain @ELSE@
        """
        if len( self._if_else_stack ) == 0:
            self.syntax_error("missing opening: @if")
        if_entry = self._if_else_stack[-1]
        inc_entry = self._include_stack[-1]
        # Toggle the state
        if_entry.state = not entry.state
        # and update the Else side
        if_entry.else_filename = inc_entry.filename
        if_entry.else_lineno = inc_entry.lineno
        self._if_else_stack[-1] = if_entry

    def _dump_ifelse(self):
        """
        We are going to die due to a syntax error.
        Dump the if_else_stack.
        """
        for n,entry in enumerate(self._if_else_stack):
            if len(entry.if_filename):
                printf("%2d) %s" % (n, entry.if_filename))
            if len(entry.else_filename):
                printf("%2d) %s" % (n, entry.else_filename))
                
    def _if_pop(self):
        """
        We have found and @endif
        """
        if len( self._if_else_stack ) == 0:
            self.syntax_error("Invalid @ENDIF@")
        self._if_else_stack.pop()
        
    def _is_if_statement( self, text ):
        """
        Determine if this text is an @if statement of some type
        """
        _ = self
        
        text = text.strip()
        if (text[0]=='@') and (text[-1]=='@'):
            pass
        else:
            return False
        # remove @ signs.
        text = text[1:-1]
        # simple else statement
        if text == 'ELSE':
            return True
        if text == 'ENDIF':
            return True
        # any type of if statement
        if text.startswith("IF_"):
            return True
        # any type of else_if statement
        if text.startswith("ELSE_IF_"):
            return True
        # not an else or an if.
        return False

    def _if_evaluate( self, text ) -> list[str]:
        """
        We have found an @IF/ELSE/ENDIF()@ Of some type
        Evaluate the expression

        Return TRUE if it is an if/else/endif type line.
        Return FALSE if it is not.
        """
        orig_text = text
        text = text.strip()
        if text.startswith('@') and text.endwith('@'):
            pass
        else:
            # must start/end with an @
            return [text]
        # remove leading/trailing @ signs.
        text = text[1:-1]
        # Simple and Basic "@ELSE@" statement
        if text == 'ELSE':
            self._else_toggle()
            result = [self._comment_where(), self._comment("ELSE") ]
            return result
        # simple and basic ENDIF
        if text == 'ENDIF':
            self._if_pop()
            return [ self._comment_where(), self._comment("ENDIF") ]

        # this must be an IF of some type
        lhs = text.find('(')
        if (lhs < 0) or (text[-1] != ')'):
            self.syntax_error("@if type things require ()s,found: %s" % orig_text)
        param = text[lhs:-1]
        if '$' in param:
            param = self.resolve_text( param )
        func  = text[0:lhs]
        # it could be any combination of:
        #    @ELSE, @ELSE_IF
        #    @IF_DEFINED, @IF_NOT_DEFINED
        #    @IF_EQUAL, @IF_NOT_EQUAL, case or no case
        is_defined = False
        is_not = False
        is_equal = False
        is_else = False
        is_case = True
        # Can it be an ELSE_IF?
        if func.startswith("ELSE_"):
            #    @ELSE_IF_DEFINED(
            # or @ELSE_IF_NOT_DEFINED(
            # or @ELSE_IF_EQUAL...
            is_else=True
            # remove "ELSE_"
            func = func[5:]
            
        if not func.startswith( "IF_"):
            self.syntax_error("not an IF_ type: %s" % orig_text )
        # could be an IF_NOT type.
        if func.startswith( "IF_NOT_" ):
            is_not = True
            # remove "IF_NOT_"
            func = func[7:]
        else:
            is_not = False
            # remove "IF_"
            func = func[3:]
        if func.startswith("EQUAL_"):
            # remove "EQUAL_"
            func = func[6:]
            # Look for the type of equal
            if func == "CASE":
                is_equal = True
                is_case = True
            elif func == "NOCASE":
                is_equal = True
                is_case = False
            else:
                self.syntax_error("Unknown IF_EQUAL: %s" % orig_text)
            if ',' not in params:
                self.syntax_error("params require a comma: %s" % orig_text )
            a,b = params.split(',',1)
            a = a.strip()
            b = b.strip()
            if is_case:
                # do not ignore case
                pass
            else:
                # Ignore case
                a = a.lower()
                b = b.lower()
            result = (a == b)
        elif func == 'DEFINED':
            params = params.strip()
            result = self._shell_vars.is_defined(params)
        result = result ^ is_not
        if is_else:
            self._elif_set( result )
        else:
            self._if_push( result )
        # We handled this line.            
        return [ self._comment_where(), self._comment("if=TRUE")]

    def _comment( self, txt ) -> str:
        """
        Given text return a comment string of that text.
        """
        assert( isinstance( self._comment_fmt, str ) )
        return self._comment_fmt % txt

    def _comment_where( self ) -> str:
        """
        Return the current infilename:LINENO as a comment.
        """
        ientry = self._include_stack[-1]
        return self._comment("%s:%d: " % (ientry.filename, ientry.lineno))
    

    def read_input(self,filename):
        """
        Read the input file.
        """
        self._include_stack.open( filename )


    def _next_line( self ) -> str|None:
        """
        Pulls next line of text from the current input file
        """
        # NOTE: lineno here is 1 based
        #       Array indexes are 0 based
        #       So we use <= as the test.
        while True:
            # Are we done?
            if len(self._include_entry) == 0:
                # Then return None
                return None
            # get the include entry...
            inc_entry = self._include_stack[-1]
            # And determine if we have reached the end of the lines.
            if_entry = self._if_else_stack[-1]

            if inc_entry.lineno > len(inc_entry.in_lines):
                # YES, so pop the include stack
                self._include_pop()
                # and loop for next line
                continue
            else:
                break

        self.fatal_where_lineno( inc_entry.lineno )
        # Success, bump lineno
        inc_entry.lineno = lineno + 1
        self._inlude_stack[-1] = inc_entry
        text = inc_entry.in_lines[ lineno-1 ]
        return text
        
    def write_output(self,filename):
        self._output.open( filename )
        self.verbose_print(0,"Writing: %s" % filename )
        fh = open( filename, "wt" )
        while True:
            # Read the next line to process.
            self._output_flush()
            text = self._next_line()
            # None means EOF.
            if text is None:
                break
            # if it is an IF/ELSE type statement.
            if not self._is_if_statement(text):
                self._output_line( self._comment_where() )
                self._output_line( self._comment( text )  )
                self._if_evaluate( text )
                continue

            result = self._process_at_name_at( text )
            # That may have returned one line, or many lines.
            if isinstance( result, str ):
                self._output_line( result )
                continue
            # many line case
            if isinstance( result, (list,tuple)):
                for text in result:
                    assert( isinstance( text, str ) )
                    self._output_line( text )
            else:
                self.fatal("process_at_name_at() did not return a string.\nresult=%s" % str(result))
        self.verbose_print(0,"Close: %s" % filename )
        fh.close()
        fh = None


class TestTemplate(unittest.TestCase):
    def __init__(self,*args,**kwargs):
        unittest.TestCase.__init__(self,*args,**kwargs)
    def tst_i_filename( self,name ):
        tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test-in")
        return os.path.join( tmp, name )
    def tst_o_filename( self, name ):
        tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test-out")
        if not os.path.isdir(tmp):
            os.makedirs(tmp)
        return os.path.join( tmp,name)
    def tst_e_filename( self,name):
        tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test-expected")
        tmp = os.path.join( tmp,name)
        assert os.path.isfile(tmp)
        return tmp
    
    def test_n001(self):
        fn_in = self.tst_i_filename("test001.txt")
        fn_out = self.tst_o_filename("test001.txt")
        template = Template()
        template.read_input(fn_in)
        template.write_output(fn_out)
        fn_expected = self.tst_e_filename("test001.txt")
        result = filecmp.cmp(fn_out, fn_expected, shallow=False)
        if not result:
            print(" GOT: %s" % fn_out)
            print("WANT: %s" % fn_expected)


if __name__ == "__main__":
    ut = TestTemplate()
    ut.test_n001()


