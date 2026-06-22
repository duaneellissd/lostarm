#
import os
import re
import time
import sys
import platform
import socket
from collections.abc import Callable
import getpass

from lostarm import verbose_print, fatal

re_var = re.compile(r"^(?P<lhs>.*)[$][{](?P<var_name>[A-Za-z_][A-Za-z0-9_]*)[}](?P<rhs>.*)$")
re_func = re.compile(r"^(?P<lhs>.*)[$][{](?P<func_name>[A-Za-z_][A-Za-z0-9_]*)(?P<params>[(].*[)])[}](?P<rhs>.*)$")

__all_functions : dict[str,"func_entry"]= {}
class func_entry():
    def __init__( self, name : str, callable_thing : Callable, n_params : int  ):
        self.name = name
        self.n_params = n_params
        self.callable_thing = callable_thing
    def call_this( self, params ) -> str:
        # Call this function pass parameters and return the result.
        params = params.strip()
        if self.n_params == 0:
            if len(params) != 0:
                fatal("%s() does not take parameters" % self.name )
            return self.callable_thing()
        if self.n_params == 1:
            return self.callable_thing( params )
        args = params.split(',')
        if self.n_params != -1:
            if len(args) != self.n_params:
                fatal("%s() requires %d parameters, got: %s" % (self.name, self.n_params, params) )
        return self.callable_thing( *args )

def _register_function( name : str, function : Callable, param_count : int ):
    global __all_functions
    __all_functions[ name ] = func_entry( name, function, param_count)

_register_function( "os.getcwd", os.getcwd, 0 )
_register_function( "os.path.abspath", os.path.abspath, 1 )
_register_function( "os.path.relpath", os.path.relpath, 1 )
_register_function( "os.path.basename", os.path.basename, 1 )
_register_function( "os.path.dirname", os.path.dirname, 1 )
_register_function( "os.path.expanduser", os.path.expanduser, 1 )
_register_function( "os.path.expand_env_vars", os.path.expandvars, 1 )

_register_function( "os.path.getsize", os.path.getsize, 1 )
_register_function( "os.path.realpath", os.path.realpath,1 )
_register_function( "os.path.samefile", os.path.samefile, 2 )
_register_function( "os.path.splitext", os.path.splitext, 1 )
_register_function( "os.path.splitroot", os.path.splitroot, 1 )

_register_function( "time.ctime", time.ctime, 1 )

time_once = None
def _time_wrapper():
    global time_once
    if time_once is None:
        time_once = str(int(time.time()))
    return time_once
_register_function( "time.time_int", _time_wrapper, 0 )

_YYYYMMDDSS_HHMMSS_once = None

def _time_YYYYMMDDSS_HHMMSS() -> str:
    global _YYYYMMDDSS_HHMMSS_once
    if _YYYYMMDDSS_HHMMSS_once is None:
        _YYYYMMDDSS_HHMMSS_once = time.strftime("%Y%m%d_%H%M%S")
    return _YYYYMMDDSS_HHMMSS_once
_register_function( "time.YYYYMMDDSS_HHMMSS", _time_YYYYMMDDSS_HHMMSS, 0 )

_register_function( "str.upper", str.upper, 1 )
_register_function( "str.lower", str.lower, 1 )
_register_function( "str.upper", str.upper, 1 )
_register_function( "str.upper", str.upper, 1 )
_register_function( "str.join", str.join, -1 )

_register_function( "str.capitalize", str.capitalize, 1 )
_register_function( "str.lstrip", str.lstrip, 1 )
_register_function( "str.rstrip", str.rstrip, 1 )
_register_function( "str.strip", str.strip, 1 )
_register_function( "str.replace", str.replace, 2 )
def _get_username():
    return getpass.getuser()
_register_function( "get_username", _get_username, 0 )
_register_function( "platform.system", platform.system, 0 )
_register_function( "platform.node", platform.node, 0 )
_register_function( "platform.system", platform.system, 0 )
_register_function( "socket.gethostname", socket.gethostname,0 )



def _function_call( m : re.Match ) -> str:
    name = m['func_name']
    params = m['params']
    entry = __all_functions.get( name, None )
    if entry is None:
        fatal("%s(%s) does not exist" % (name,params))
    return entry.call_this( params )


class Variables():
    def __init__( self ):
        self.vars = dict()
        self.use_env = True
        self.re_def_is_fatal = True
        self.re_def_is_warning = True
        self._r_history = []
        
    def _dump_history( self ):
        """
        Print the history of the variable resolution
        """
        for n, s in enumerate(self._r_history):
            verbose_print(0, "%2d) %s" % (n,s))

    def add_variable( self, name, value ) -> None:
        """
        Define a variable
        Example: Support a command line defined variable.
        """
        if name in self.vars:
            if self.re_def_is_fatal or self.re_def_is_warning:
                verbose_print(1,"Redefined=%s" % name)
                verbose_print(1,"old: %s=%s" % (name,self.vars[name]))
                verbose_print(1,"new: %s=%s" % ( name,value ))
            if self.re_def_is_fatal:
                fatal("Sorry, that is fatal")
        self.vars[name] = value

    def value_of( self, name ) -> str:
        """ 
        Return the value of the variable: "name"
        If not defined, fatal error.
        """
        value = ""
        if name in self.vars:
            value = self.vars[name]
        elif self.use_env:
            if name in os.environ:
                return os.environ[name]
        else:
            self._dump_history()
            fatal("undefined: %s" % name )
        return value
    
    def resolve( self, text : str ) -> str:
        """
        Replace all ${VARIABLES} in the string.
        Replace all ${FUNC(calls)} in the string.
        """

        self._r_history = []
        while True:
            self._r_history.append( text )
            if len(self._r_history) > 50:
                self._dump_history()
                fatal("string does not resolve after 50 rounds")
            m = re_var.match( text )
            if m:
                lhs = m['lhs']
                name = m['var_name']
                rhs = m['rhs']
                value = self.value_of(name)
                text = lhs + value + rhs
                # Try for next variable.
                continue
            # Ok no simple vars try function calls.
            m = re_func.match(text)
            # If this is Non
            if m is None:
                # Success!
                self._r_history = [] # release memory.
                return text
            value = _function_call( m )


