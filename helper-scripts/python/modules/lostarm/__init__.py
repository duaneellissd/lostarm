import sys

class Utils():
    def __init__( self ):
        self._verbose_level = 0
        
    def fatal( self, msg ):
        _ = msg
        print( msg )
        sys.exit(1)

    def fatal_here( self, filename, lineno, msg ):
        _ = self
        print("%s:%d: Fatal: %s" % (filename,lineno,msg ) )

    def set_verbosity( self, level ):
        self._verbose_level = level

    def inc_verbosity( self, amount ):
        self.set_verbosity( self._verbose_level + amount )

    def verbose_print( self, level, msg ):
        if (level == 0) or (level < self._verbose_level):
            print( msg )

_singleton = Utils()

def set_verbosity( level : int ):
    _singleton.set_verbosity(level)

def inc_verbosity( amount : int ):
    _singleton.inc_verbosity(amount)

def parse_verbose( args : list ) -> list:
    result = []
    for tmp in args:
        if tmp == '-v':
            inc_verbosity(1)
        else:
            result.append( tmp )
    return result

def fatal( msg ):
    _singleton.fatal(msg)

def fatal_here( filename, lineno, msg ):
    _singleton.fatal_here( filename, lineno, msg )

def verbose_print( level : int, msg : str ):
    _singleton.verbose_print( level, msg )
