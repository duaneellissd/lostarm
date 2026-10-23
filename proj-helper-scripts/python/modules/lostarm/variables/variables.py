import re
import socket
import sys
import getpass
import os
import time

from lostarm.utils import VerbosePrint

__ALL__ = ['Variables', 'get_global_vars',
    "VarError", "VarSyntaxError", "Var_UndefinedFunc", "Var_UndefinedVar",
    "Var_RecursionError", "Var_DuplicateError"]

def my_extension(s: str):
    parts = os.path.splitext(s)
    return parts[1]


def no_extension(s: str):
    parts = os.path.splitext(s)
    return parts[0]


def stat_st_mtime(s: str):
    s = os.stat(s)
    return s.st_mtime


def stat_st_size(s: str):
    s = os.stat(s)
    return s.st_size


func_table = {
    "str.upper": (str.upper, "s"),
    "str.lower": (str.lower, "s"),
    "str.endswith": (str.endswith, "s"),
    "str.startswith": (str.startswith, "s"),
    "str.find": (str.find, "s"),
    "str.isalpha": (str.isalpha, "s"),
    "str.isalnum": (str.isalnum, "s"),
    "str.isascii": (str.isascii, "s"),
    "str.isdecimal": (str.isdecimal, "s"),
    "str.isdigit": (str.isdigit, "s"),
    "str.islower": (str.islower, "s"),
    "str.isupper": (str.isupper, "s"),
    "str.join": (str.join, "s,l"),
    "str.lstrip": (str.lstrip, "s"),
    "str.rstrip": (str.rstrip, "s"),
    "str.strip": (str.strip, "s"),
    "str.removeprefix": (str.removeprefix, "s,s"),
    "str.removesuffix": (str.removesuffix, "s,s"),
    "str.replace": (str.replace, "s,s"),
    "len": (len, "s"),
    "os.getcwd": (os.getcwd, ""),
    "os.path.abspath": (os.path.abspath, "s"),
    "os.path.join": (os.path.join, "*"),
    "os.path.dirname": (os.path.dirname, "s"),
    "os.path.basename": (os.path.basename, "s"),
    "os.path.getsize": (os.path.getsize, "s"),
    "os.path.isdir": (os.path.isdir, "s"),
    "os.path.normcase": (os.path.normcase, "s"),
    "os.path.normpath": (os.path.normpath, "s"),
    "os.path.realpath": (os.path.realpath, "s"),
    "pathtool.extension": (my_extension, "s"),
    "pathtool.no_extension": (no_extension, "s"),
    "stat.st_mtime": (stat_st_mtime, "s"),
    "stat.st_size": (stat_st_size, "s")
}


class VarError(Exception):
    '''
    A common Exception for all VAR errors.
    (so you can catch one, not many errors)
    '''
    SYNTAX = 1
    UNDEF_FUNC = 2
    UNDEF_VAR = 3
    RECURSION = 4
    DUPLICATE = 5

    def __init__(self, typecode: int, msg: str, history: list):
        m = [msg]
        for n, h in enumerate(history):
            m.append("%d) %s" % (n, h))
        m = '\n'.join(m)
        Exception.__init__(self, m)
        self.msg = m
        self.history = history
        self.typecode = typecode


class Var_SyntaxError(VarError):
    '''
    Raised when we find an obvious syntax error.
    '''

    def __init__(self, history: list, text: str):
        VarError.__init__(self, VarError.SYNTAX, "Syntax error: %s" % text, history)
        self.text = text


class Var_UndefinedFunc(VarError):
    '''
    Raised when an undefined variable function is called.
    '''

    def __init__(self, name: str, history: list):
        VarError.__init__(self, VarError.UNDEF_FUNC, "undefined function: %s" % name, history)
        self.name = name


class Var_UndefinedVar(VarError):
    '''
    Raised when an undefined variable is referenced
    '''

    def __init__(self, name: str, history: list):
        VarError.__init__(self, VarError.UNDEF_VAR, "ERROR undefined var: %s" % name, history)
        self.name = name


class Var_RecursionError(VarError):
    '''
    Raised when a variable is recursive
    example: ${A}->${B}->${A} endlessly.
    '''

    def __init__(self, history: list[str]):
        VarError.__init__(self, VarError.RECURSION, "Recursive stop %d tries" % len(history), history)


class Var_DuplicateError(VarError):
    '''
    Raised when defining a variable and it is a duplicate
    '''

    def __init__(self, new_name : str, old_name : str, history : list[str] ):
        # One day, the new/old will have "where defined" attribute.
        VarError.__init__(self, VarError.DUPLICATE,
                          "Duplicate variable: %s" % new_name, history)
        self.new_name = new_name
        self.old_name = old_name

# SIMPLE-MATCH:
#   Match <LHS> ${ CONTENT } <RHS>
#   Note: LHS or RHS might be empty.
_re_simple_var = re.compile(r'(?P<LHS>^.*)[$][{](?P<CONTENTS>.*)[}](?P<RHS>.*$)')
# Match a function call like: ${os.path.abspath(${OBJ_DIR})}
#   note that: ${OBJ_DIR} would be resolved first...
#   Then the function os.path.abspath() would be called.
_re_function_call = re.compile(r'^(?P<fname>[a-zA-Z_][A-Z0-9a-z_.]*)[(](?P<params>.*)[)]$')
# This matches a basic variable name, ie: ${OBJ_DIR}
# used to determine if we have a VARNAME or FUNCTION_CALL
_re_basic_name = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

# These are variables we do not want the user to use.
# The KEY is the bad (not-desired) name, the value is error message
_bad_var_names = {
    "__file__" : "Do not use ${__file__}, use ${__FILE__} instead"
}

class _resolver(VerbosePrint):
    '''
    This is the variable resolver.
    You don't use this directly, the Variable class uses this to resolve vars.
    Generally, the idea is to call: "_resolver.do_pass()" in a loop.
    '''

    def __init__(self, parent, starting_text, vars: dict):
        VerbosePrint.__init__(self)
        self._parent = parent
        self._vars = vars
        self.history = [starting_text]

    def _do_replacement(self, lhs, value, rhs):

        result = lhs + value + rhs
        self.history.append(result)
        return (True, result)

    def _basic_var(self, lhs, varname, rhs):
        '''
        Once a basic variable is found, this does the replacement.
        '''
        if varname in _bad_var_names:
            self.fatal("Sorry: %s" % _bad_var_names[ varname ] )
        if str(varname) not in self._vars:
            e = Var_UndefinedVar(varname, self.history)
            self._parent.fatal(e)
            # raise e
        value = self._vars.get(varname, None)
        result = self._do_replacement(lhs, value, rhs)
        return result

    def _get_params(self, fname: str, fentry: dict, param_text: str):
        '''
        Given the function table entry (a tuple)
        Where: fentry[0] = the function pointer
        And:   fentry[1] = the parameter list.
        RETURN an LIST of parameters.

        TODAY: I am a lazy bastard, so we split on commas
        FUTURE: we might add quoted strings and fancy stuff
        '''
        # Just split our params up simple style.
        if len(param_text) == 0:
            our_params = []
        else:
            our_params = param_text.split(',')

        # TODO:
        #    Determine what the actual implementation requires.
        #    For some detail, see:
        #        https://docs.python.org/3/library/inspect.html
        # The idea is some type of syntax checking..

        return our_params

    def _do_function_call(self, lhs, func_match, rhs):
        '''
        This handles a function call, for example: ${str.upper(${A})}
        '''
        fname = func_match['fname']
        if fname not in func_table:
            raise Var_UndefinedFunc(fname, self.history)
        entry : dict = func_table.get(fname)
        param_list = self._get_params(fname, entry, func_match['params'])
        func_ptr = entry[0]
        result = func_ptr(*param_list)
        if not isinstance(result, str):
            result = str(result)
        text = self._do_replacement(lhs, result, rhs)
        return text

    def do_pass(self, text):
        '''
        this performs the simple and function type replacement.
        This does ONE and only ONE replacement.
        This function returns a tuple, (BOOL, Result)
        This function also tracks "history"
        where:
           Result is the current text string.
           BOOL is TRUE if a replacement was made (forward progress)
           BOOL is FALSE if no replacement was found (ie: done)
        '''
        # stop the recursive case where:  ${A}->${B}->${A} endlessly.
        if len(self.history) > 20:
            raise Var_RecursionError(self.history)
        lh_loc = 0
        rh_loc = len(text)
        done = False
        while not done:
            start = text.find("${", lh_loc)
            if start < 0:
                # No further progress can be made.
                return (False, text)
            # See if there is another further ahead, ie: ${${inside}}
            tmp = text.find("${", start + 2)
            if tmp >= 0:
                # There is another var so keep searching
                lh_loc = tmp  # +2 skips the opening ${
                continue
            done = True
            lh_loc = start
        # find the closing curly brace
        rh_loc = text.find('}', lh_loc)
        if rh_loc < 0:
            # Missing closing curly brace?
            raise Var_SyntaxError(self.history, text)
        lhs = text[0:lh_loc]  #
        # The +2 skips the opening ${
        varname = text[lh_loc + 2:rh_loc].strip()
        rhs = text[rh_loc + 1:]  # +1 skips the } close.
        if _re_basic_name.match(varname):
            return self._basic_var(lhs, varname, rhs)

        # If not a var, is this a function call?
        content = varname.strip()
        # FUTURE: support NESTED function calls??
        # ie:  ${os.path.abspath(os.path.join('dog','cat','frog'))}
        func_match = _re_function_call.match(content)
        if func_match is not None:
            # YES - then do the function call.
            return self._do_function_call(lhs, func_match, rhs)
        # otherwise it is a syntax error.
        raise Var_SyntaxError(self.history, text)



class Variables(VerbosePrint):
    '''
    This gives a crude "shell-like" text variables with some functions.
    Example:
        dog_name=Walter
        the text: "My Dog's name is ${dog_name}"
        when resolved, would be: "My Dog's name is Walter"
    '''

    def __init__(self):
        VerbosePrint.__init__(self)
        self._vars = dict()
        self._once_vars = dict()

    def add_default_vars(self):
        self.add_variable( "CWD", os.getcwd() )
        self.add_variable( "HOSTNAME", socket.gethostname() )
        self.add_variable( "USER", getpass.getuser() )
        tmp = os.path.abspath(sys.argv[0])
        self.add_variable( "TOOL_ABS_PATH", tmp  )
        self.add_variable( "TOOL_DIR", os.path.dirname( tmp ) )
        self.add_variable( "UNIX_TIME", str(int(time.time())) )
        self.add_variable( "CTIME", time.strftime("%c", time.localtime()) )

    def reset(self):
        self._vars = dict()

    def items(self):
        return self._vars.items()

    def fatal(self, the_exception : Exception) -> None:
        self.fatal_or_raise( the_exception )

    def replace(self, name, value):
        '''
        Replace the definition of this var.
        '''
        if name in _bad_var_names:
            raise Exception("Bad variable '%s' ->%s" % (name,_bad_var_names[name]))
        assert( name not in self._once_vars )
        self._vars[name] = value

    def add_variable_once(self, name, value ):
        """
        There are some variables we want set once and only once.
        For example a ${TIME_NOW} variable contains the current time
        in seconds. As the tool runs, the current time changes.
        ie: 12:34:56 becomes 12:34:57...

        And some other module might - during its initialization process
        might choose to set the time again - we might not want that.

        Thus, if you call add_variable_once( "TIME_NOW", value )
        and something had already set the time you do not have
        that drifting clock problem.

        That is not always what we want.
        """
        if name in _bad_var_names:
            raise Exception("Bad variable '%s' ->%s" % (name,_bad_var_names[name]))
        if name in self._once_vars:
            # Ignore a second time.
            return
        # do not repeat.
        self._once_vars[name] = value
        # and set the value of the variable.
        if name not in self._vars:
            self._vars[name] = value

    def add_variable(self, name : str, value :str ) -> None:
        if name in self._vars:
            old = self._vars[name]
            raise Var_DuplicateError(name, old, [])
        self.replace(name, value)

    def resolve_all_vars(self):
        for n,v in self._vars.items():
            self.replace(n, self.resolve_text(v))

    def add_dict(self, some_dict):
        """
        Given a dict of vars, ie: "name" : "value" add these.
        """
        for k, v in some_dict.items():
            self.add_variable(k, v)

    def resolve_text(self, text):
        '''
        Given text in the form: "hello ${planet}" perform var replacement.
        Also handles: "hello ${str.upper(${planet})}"
        '''
        tmp = _resolver(self, text, self._vars)
        progress = True
        while progress:
            (progress, text) = tmp.do_pass(text)
        return text
    def save_as_dict(self):
        """
        this is used when we are saving state to a file
        and need to preserve the vars and the OnceVars
        """
        result = dict()
        result['VARS'] = self._vars.copy()
        result['ONCE_VARS'] = self._once_vars.copy()
        return result
    def load_as_dict(self, data: dict) -> None:
        """ 
        Used in reverse of "save_as_dict" above.
        """
        if 'VARS' not in data:
            self.fatal("Cannot load missing key: VARS")
        if 'ONCE_VARS' not in data:
            self.fatal("Cannot load missing key: ONCE_VARS")
        self._vars = data['VARS'].copy()
        self._once_vars = data['ONCE_VARS'].copy()

# This provides a single common set of ${VARS}
_global_vars = Variables()

def get_global_vars() -> Variables:
    return _global_vars

