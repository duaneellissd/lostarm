import json
import os
import sys
__ALL__=['Jproject']

from jproject.keys import KEYS

def _is_string_array( value : (str|list[str])) -> bool:
    """
    Somethings might be a simple list of strings or a simple string.
    This helps us know what it is.
    """
    if not isinstance( value, ( list, tuple ) ):
        return False
    for this_value in value:
        if not isinstance( this_value, str ):
            return False
    return True

class Jproject():
    """
    This defines JSON Project.
    
    A JSON Project defines an "app" (an exe file) or a "lib" (a static/shared library)

    This portion of the tool reads and parses json definition files.
    ====
    In this module, a KEY is an expected KEY to be found in 2 places.
    Place #1 - is in the input json (jproject) file.
    Place #2 - in the output "self._jproject" dictionary.

    """
    # this identify the key types that hold a path
    # Generally paths must be converted to ABSPATH
    # 
    path_like_KEYS = (
        KEYS.PROJ_ROOT_DIR,
        KEYS.ENV_VARS,
        KEYS.MAKE_VARS,
        KEYS.LINKER_SCRIPT,
        KEYS.PRE_BUILD_SCRIPT,
        KEYS.POST_BUILD_SCRIPT
    )

    type_app_or_lib = [ KEYS.STR_app, *KEYS.STRS_libs ]
    type_lib_only = KEYS.STRS_libs

    # What files do we normally exclude in a source/header file search.
    std_excludes = "*.doc;*.docx;*.pdf;*.txt;*.md".split(';')

    
    # when given just an inc path as a string expand it like this
    default_CMDLINE_INC_DIRS = {
        KEYS.CLSID_path : "tbd",
        KEYS.CLSID_exclude_pattern  :  std_excludes,
        KEYS.CLSID_isinclude : True,
        KEYS.CLSID_include_pattern : "*.h;*.hxx;*.hh"
    }

    # When given just a source path as a string, expand it to this
    default_SRC_DIRS = {
        KEYS.CLSID_path : "tbd",
        KEYS.CLSID_exclude_pattern  :  std_excludes,
        KEYS.CLSID_isinclude : True,
        KEYS.CLSID_include_pattern : "*.h;*.hxx;*.hh"
    }

    def __init__( self ):
        """ the data we are collecting goes here"""
        self._jproject : dict = dict()
        """ The ABS path to the current JSON file we are parsing """
        self._cur_filename : str = ""
        """ The line number of/in the current JSON file we are parsing """
        self._cur_lineno : int = 1
        # Sadly the standard lib json does not provide line numbers
        # So we just use a single line number 1 for error locations.
        """This include sack supports the KEY.INCLUDE_JSON directive"""
        self._include_stack : list = []
        self._dumped_include_stack = False
        self._vars = Variables()

    def add_var( self, )

    def _dump_include_stack(self) -> None:
        """
        When parsing INCLUDE_JSON we often have fatal errors.
        This dumps the include stack to the console like a C compiler does.
        """
        if self._dumped_include_stack:
            return
        # DO NOT REPEAT
        self._dumped_include_stack = True
        for (fn,ln) in self._include_stack:
            self.not_fatal("%s:%d - Include from here" % (fn,ln))
                        
        
    def fatal_here(self, msg : str ) -> None:
        """
        Parsing has gone bad we are giving up
        """
        self._dump_include_stack()
        self.not_fatal_here( msg )
        # This is fatal so we die a horrible death.
        sys.exit(1)

    def not_fatal_here( self, msg : str) -> None:
        """
        Parsing has failed, we are giving up.
        But we are not dead yet.... we have more error messages to print.
        Used in conjunction with self.not_fatal_here()
        """
        self._dump_include_stack()
        print("%s:%d: FATAL: %s" % (self._cur_filename, self._cur_lineno), msg )

    def not_fatal( self, msg : str ) ->None:
        """
        Like self.not_fatal_here, does not include the filename/lineno
        Does not exit, used in conjunction with self.fatal()
        """
        self._dump_include_stack()
        print(msg)
        
    def fatal( self, msg : str ) -> None:
        """
        Parsing has failed.. exit.
        """
        self._dump_include_stack()
        self.not_fatal(msg)
        sys.exit(1)
        
    def _include_push(self, new_filename : str)->None:
        """
        handles push/pop for the INCLUDE_JSON statement
        """
        self.include_stack.append( (self._cur_filename, self._cur_lineno) )
        if len( self.include_stack ) > 50:
            # this just an arbitrary reasonable limit
            self.fatal_here("Include stack overflow")
        self._cur_filename = new_filename

    def _include_pop( self ) -> None:
        """
        Remove an entry from the include stack
        """
        (self._cur_filename, self._cur_lineno) = self.include_stack.pop()

    def relative_to_cur_json(self, filename : str ) -> str:
        """
        some json is referencing some other file
        That file is relative to that json file.
        
        So convert this filename into an abspath
        """
        # if it is already abs..
        if self._cur_filename is None:
            return os.path.abspath( filename )
        if not os.path.isabs(filename):
            # We are within a json file so we have 
            dname = os.path.dirname( self._cur_filename )
            # combine the two.
            filename = os.path.abspath( os.path.join( dname, filename ) )
        # And ABS the filename
        return os.path.abspath( filename )

    def load_root_project( self, filename : str ) -> None:
        """
        This is the main entry point for jproject.
        One JSON file is defined as the root project.
        That root JSON file uses: INCLUDE_JSON to include other files.

        This loads the base project and expands all included json files.
        The result is self._jproject holds the project.
        """
        self._jproject = dict()
        self.include_stack = []
        self._merge_json_file( filename, KEYS.STRS_app_or_libs );

    def _merge_json_file( self, filename : str, types_allowed : (str|list|tuple) ) -> None:
        filename = self.relative_to_cur_json( filename )
        if not os.path.isfile(filename):
            self.not_fatal("cwd: %s" % os.getcwd())
            self.fatal("%s: No such file or directory" % filename )
        txt = ''
        self._include_push(filename)
        with open( self._cur_filename, "rt" ) as f:
            txt = f.read();
        # load via stdlib parser.
        try:
            data = json.loads( txt )
        except json.JSONDecodeError as e:
            self.not_fatal("%s:%d: %d json parse error: %s" % (filename, e.lineno, e.colno, e.msg) )
            self.fatal("sorry")
        actual_type = data.get( KEYS.PROJ_TYPE, None)
        if actual_type is None:
            self.fatal_here("Missing key: %s" % KEYS.PROJ_TYPE )
        if actual_type not in types_allowed:
            self.fatal_here("Type: %s is not one of: %s" % (actual_type, str(types_allowed)))
        self._merge_json_data( data )
        self._include_pop()
       
    def _merge_json_data( self, data_to_merge : dict ) -> None:
        """
        Given a new JSON dict merge the items into the self._jproject 
        Each type of element might have various merge rules.
        """
        # simple loop over and merge key/value pair.
        for k,v in data_to_merge.items():
            # this function handles any unique ways we need to merge keys.
            self._merge_this_key( k, v )

    def _merge_this_key( self, keyname, value ):
        """
        Handle each special case of merging an item.
        """
        if keyname == KEYS.PROJ_TYPE:
            if len(self._include_stack) == 1:
                # We are in the top most [root] JSON file
                self._merge_key_string( keyname, value )
                return
            # Ok we are "deep" so we only accept libs.
            if value in KEYS.STRS_libs:
                # ignore this
                return
            self.fatal_here("SUB jproject projects can [currently] only be one of: %s" % ",".join(KEYS.STRS_libs))

        # We use the "KEYNAME" to find handler
        #========================================
        # given a name: "FOO"
        # attempt to locate: self._handle_FOO
        tmp = "_handle_%s" % keyname
        callable = None
        try:
            callable = self.__getattribute__( tmp )
        except KeyError:
            callable = None
        if callable is None:
            # no such thing exists so treat it as a simple string.
            if isinstance( self, str ):
                self._merge_key_string( keyname, value )
                return
            if _is_string_array( value ):
                self._merge_key_string( keyname, value )
                return
            if keyname not in self._jproject:
                    self._jproject[ keyname ] = value[:]
                    return
            
        if callable is not None:
            # We found one! call that function.
            callable( keyname, value )
            return
        # We do not know how to handle it we are dead.
        self.fatal_here("Unknown key: %s" % keyname )

    def provide_default( self, keyname, value ):
        """
        if the key does not yet exist, create it with this value.
        """
        assert( keyname not in self._jproject )
        self._jproject[ keyname ] = value
      
    def _merge_key_string( self, keyname, value ):
        """
        This keyname is a simple string, there should not be duplicates.
        Example:
             "PROJ_NAME" = "my_great_project"
        """
        # check for duplicate
        if keyname not in self._jproject:
            self._jproject[keyname] = value
            return
        old_value= self._jproject[keyname]
        if _is_string_array( old_value ):
            # and new thing is string, just append it.
            if isinstance( value, str ):
                self._jproject[keyname].append( value )
                return
            # If new thing is a string array extend it.
            if _is_string_array( value ):
                self._jproject[keyname].extend( value )
                return
        # We do not know what to do so bail out.
        self.not_fatal_here("Cannot determine how to merge duplicate key: %s" % keyname )
        self.not_fatal_here("old-value: %s" % str(old_value))
        self.fatal_here(    "new-value: %s" % str(value))

    def validate_DICT_DIR( self, keyname : str, value : (dict|str), parent_key : str, default_values : dict ) -> None:
        """
        Give a CMDLINE_INC_DIR or SRC_DIRS
        Add it to the JPROJECT
        BUT - also fill in all the default values for the thing in case they are missing.
        And make sure there are not surprises (extra stuff we do not know about)
        """

        if parent_key not in self._jproject:
            self._jproject[ parent_key ] = []
        # This is what we are creating.
        result = dict()
        # be kind, accept simple things in the json.
        if isinstance( value, str ):
            result[KEYS.CLSID_path] = value
        # it must otherwise be a dict.
        if not isinstance( value, dict ):
            self.fatal_here( "Not a dict: %s=%s" % (keyname, str(value)))
        # get list of keys we will accept.
        expected_keys = list(default_values.keys())
        # go through actual keys in the entry
        for k,v in value.items():
            if k not in expected_keys:
                self.fatal_here("Unknown key: %s, value=%s" % (k,v))
        for k,v in default_values.items():
            # This is special cased
            # it is the directory or a source filename.
            if k == 'path': 
                continue
            if k in value:
                # already present use what was given.
                result[k] = value[k]
                continue
            else:
                # not present, then use the default value
                result[k] = v
            continue
        for tmp  in self._jproject[ parent_key ]:
            if tmp[ KEYS.CLSID_path ] == result[ KEYS.CLSID_path ]:
                print("Duplicate:")
                print( str( tmp ) )
                print( result )
                if 'dup' not in tmp:
                    tmp['dup'] = []
                    tmp['dup'].append( result )
                    break
            self._jproject[ parent_key ].append( result )

    def _validate_CMDLINE_INC_DIRS( self, keyname, value : (dict|str)) -> None:
        """
        Given a simple path - return a cmdline_inc_dir dict.
        Given a dict make sure it is a cmdline_inc_dir
        And add defaults for things that are missing.
        """
        self.validate_DICT_DIR( keyname, value,KEYS.CMDLINE_INC_DIRS, self.default_CMDLINE_INC_DIRS )

    def _validate_SRC_DIRS( self, keyname : str,value : (dict|str) ) -> None:        
        self.validate_DICT_DIR( keyname, value,KEYS.SRC_DIRS, self.default_SRC_DIRS )

    def _handle_generic_DIR( self, keyname, value ) -> None:
        """
        Attempt to handle the SRC_DIRS or CMDLINE_INC_DIRS in a generic way.
        """
        result = dict()
        # Get the validator for this key
        tmp = "_validator_%s" % keyname
        # What json does not have is a 'schema' that defines
        # What should/should-not, or defaults for a json dict.
        # so we do this via the validator callback.
        validator = self.__getattr__(keyname,None)
        if validator is None:
            self.fatal("NO validator for key: %s" % keyname )
        if isinstance( value, str ):
            result = { KEYS.CLSID_path : value }
        # call the validator 
        result = validator( keyname, result )
        # if we do not have this list in the jproject add an empty one.
        if keyname not in self._jproject:
            self._jproject[ keyname ] = []
        # Append this one.
        self._jproject[ keyname ].append( result )
        
    def _handle_inc_src( self, keyname, value, validator ):
        """
        Generically handle a CMDLINE_INC_DIR or SRC_DIR
        """        
        if isinstance( value, str ):
            validator( value )
            return
        # must otherwise be a list or tuple
        if not isinstance( value, (list,tuple) ):
            self.fatal_here("Entry is not an array of (strings|dict) %s" % str(value))
        # for each thing in the list
        for thing in value:
            if isinstance( thing, (str,dict) ):
                validator(thing)
                continue
            self.fatal_here("Entry is not a str or dict, actual=%s" % str(thing) )

    def _handle_CMDLINE_INC_DIRS( self, keyname, value ):
        """
        This represents what you would know as series of: -I path -I path 
        on the compiler command line. Example:
        
           "CMDLINE_INC_DIRS" : [
                  "path1",
                  "path2"
                 ... or it could have a dict here with more details ...
           ]
        
        The dict must be in the form: self.default_

        """
        self._handle_inc_src( keyname, value, self._validate_CMDLINE_INC_DIRS )

        

    def _handle_SRC_DIRS(self, keyname, value ):
        """
         For an example: see: self.default_src_dict
        """
        self._handle_inc_src( keyname, value, self._validate_SRC_DIRS )
     

  

    

                
