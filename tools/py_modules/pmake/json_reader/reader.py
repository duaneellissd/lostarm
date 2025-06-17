import os
import pmake
import json
import copy
from typing import NoReturn

from pmake.logger import log_verbose_set

log_verbose_set(3)

class JsonReader_UnitTestError( Exception ):
    def __init__( self, short_reason : str, human_reason : str  ):
        self.short_reason = short_reason
        Exception.__init__( self, human_reason )
       

class JsonReader():
    '''
    This handles our style of "json" files
    "our syle of json files" are this:
        a)  All json files must be a dict, not a list.

        b)  There are a few reserved keys (all lower case)
            "fatal", "info", "warn", "variables", "include", and "if(...)"

        c)  The "fatal", "info", and "warn" keys expect a string message to print.
            "fatal" prints exits the application.
            "info" - just prints the message
            "warn" - outputs a warning message
        
        d)  The key 'variables' expects to resolve to a dict.
            the resulting name/value pairs become defined variables.
            
            Example:
                "variables" : {
                    "cat" : "garfield",
                    "dog" : "Walter"
                }

        b)  if a key is: "include", the value is a filename 
            This will be searched via the include path..
            The content of the "filename" must be a dict
            and it is merged/inserted in place of the "include" statement.
            See below for details about "merging a dict"
           
            Example:
                "include" : "somefile.json"

        c)  If a KEY begins with "if(" and ends with a ")"
            Meaning it looks like: "if( EXPRESSION )"
            We assume it contains an expression in the standard way.
            The value must be a DICT.

            NOTE you provide the expression evaluator as a callback.
            Your callback gets two parameters:
                evaluator( tool: Json_Tool, expression : str )
                The TOOL provides:  tool.parse_fatal( reasonword, humanmsg )
                The "reasonword" is used during unit test only
                This helps verify the types of parse errors in unit test

            Your callback must return a boolean (True or False)

            if the return value is True, the content is merged in place

            Example:
                "if( ${dog} == 'Walter' )" : {
                    "include": "walters-world.json"
                }

                "if( defined(cat) )" : {
                    "fatal" : "Walter does not like cats"
                }
            NOTE The syntax of the expression is up to your callback.

        d)  When merging a dict the content of various things (the value)
            must be a dict, and the result must not duplicate keys.

            Because JSON dicts can "re-arrange" them selves and are not order-stable
            the resulting "duplicate error" messages may come out of order.
          
    '''
    def __init__( self, if_evaluator, var_definer ):
        
        assert( callable( if_evaluator) )
        assert( callable( var_definer ) )
        self.unit_test_mode = False
        self.cur_path = []
        self.include_path = []
        self._if_eval_cb = if_evaluator
        self._var_definer = var_definer
        self._include_depth = 0

    def setNoExit( self ) -> None:
        '''
        When not in a unit test situation we want to sys.exit(1)
        
        But when running unit tests, we want fatal errors to "raise"
        So we set a flag that controls that here.
        '''
        self.unit_test_mode = True

    def add_include_path( self, path : str ) -> None:
        self.include_path.append( path )

    def _find_include_file( self, filename : str ) -> str:
        '''
        We have parsed an: "include" : "filename"
        Search the "path list" and try to find that file.
        return the resulting name
        '''
        tried = []
        pmake.debug_print(1,"Resolve-include: %s" % filename )
        for path in self.include_path:
            fn = os.path.abspath(os.path.join( path, filename ))
            # Did we find it?
            pmake.debug_print(1,"Try: %s" % fn )
            if os.path.isfile( fn ):
                # Success
                pmake.debug_print(1,"Found: %s" % fn )
                return fn
            # So sad
            tried.append(fn)
        # we are fatal now - no more places to try
        for n, path in enumerate( tried ):
            pmake.debug_print(0, "Tried: %2d) %s" % (n+1,path))
        self.parse_fatal( "FILE-NOT-FOUND", "Cannot find: %s" % filename )

    def path_push( self, txt : str ) -> None:
        self.cur_path.append(txt)
        if len(self.cur_path) < 25:
            return
        # we have gone crazy?? */
        pmake.debug_print(0,"Path depth is > %d\n" % len(self.cur_path) )
        self.parse_fatal( "PATH-DEPTH", "Fatal" )

    def path_pop(self) -> None:
        self.cur_path.pop()

    def parse_fatal( self, unittest_reason : str, human_msg : str ) -> NoReturn :
        pmake.debug_print(0,"Current path")
        for n, path in enumerate( self.cur_path ):
            pmake.debug_print(0,"%2d) %s" % (n+1,path ))
        if self.unit_test_mode:
            raise JsonReader_UnitTestError( unittest_reason, human_msg )
        else:
            pmake.fatal("%s: %s" % ('.'.join(self.cur_path), human_msg ))

    def _load_json( self, filename : str ) -> dict:
        '''
        Simple - wrap for json.loads() that prints a nice error message
        and does not produce python vomit.
        '''
        
        self.path_push( filename )
        with open( filename, "rt" ) as f:
            txt = f.read()
        try:
            content = json.loads( txt )
        except json.JSONDecodeError as E:
            pmake.debug_print(0,"%s:%d: Json parse error" % (filename, E.lineno ))
            self.parse_fatal( "JSON-ERROR", "JSON parse error: %s" % E.msg )
        if not isinstance( content, dict ):
            pmake.debug_print(0, "%s:1: Error not a dictionary" % filename )
            self.parse_fatal( "NOT-A-DICT", "Must be a dict")
        
        self.path_pop()
        return content
    
    def read_file( self, filename : str ) -> dict:
        '''
        This is the 'main entry point' for this class/module
        '''
        filename = os.path.abspath( filename )
        if not os.path.isfile(filename):
            pmake.debug_print(0,"%s:1: Not a file" % filename )
            pmake.fatal("NO-SUCH-FILE", "FATAL")
        jdata = self._load_json( filename )
        self.path_push( filename )
        result = self.resolve_json( jdata )
        self.path_pop()
        return result
    
    def resolve_json( self, jdata : dict ) -> dict:
        '''
        This resolves/converts/merges all json keywords we support are handled.
        ie: fatal, info, warn, include, variables, if()
        '''
        result = dict()
        for k,v in jdata.items():
            k = k.strip()
            if k == 'fatal':
                pmake.fatal( "FATAL-KEYWORD", v )
                continue
            if k == 'warn':
                pmake.warn_print( v )
                continue
            if k == 'info':
                pmake.debug_print(0,v)
                continue
            if k == 'include':
                content = self._handle_include_statement( v )
                result = self._merge( result, content )
                continue
            if k == 'variables':
                if not isinstance( v, dict ):
                    self.parse_fatal( "BAD-VARIABLE-DATA", "variables must be a DICT, not: %s" % str(v) )
                for subkey, subvalue in v.items():
                    self._var_definer( subkey, subvalue )
                continue
            if k.startswith("if(") and k[-1] == ')':
                expression = k[3:-1]
                try:
                    pmake.debug_print(1,"Expression: %s" % expression )
                    expression_result = self._if_eval_cb( self, expression )
                except Exception as E:
                    print("E=%s" % dir(E))
                    self.parse_fatal( "EXPRESSION-ERROR" % E.msg )
                pmake.debug_print(1,"Result: %s" % result )
                if expression_result:
                    content = self.resolve_json( v )
                    result = self._merge( result, content )
                continue
            result[ k ] = v
            continue
        return result

    def _handle_include_statement( self, filename : str ) -> dict:
        '''
        Call the basic parser recursively to handle an include statement.
        Returns a DICT that is the 'resolved' content of the include file.
        '''
        pmake.debug_print(1,"Include: %s" % filename )
  
        filename = self._find_include_file( filename )
        pmake.debug_print(1,"Resolves-to: %s" % filename )
        jdata = self._load_json( filename )
        self._include_depth += 1
        if self._include_depth > 30:
            self.parse_fatal( "INCLUDE-RECURSION", "include files are too deep (%d)" % self._include_depth)
        result = self.resolve_json( jdata )
        self._include_depth -= 1
        return result
    
    def _merge( self, dest : dict, src : dict ) -> dict:
        '''
        Givent he existing dict(dest) - merge the src(dict) into the dest
        Returns the result
        '''
        result = copy.deepcopy( dest )
        for k,v in src.items():
            if k in result:
                self.parse_fatal("DUPLICATE-KEY", "Duplicate key: %s" % k )
            result[k] = v
        return result
        
