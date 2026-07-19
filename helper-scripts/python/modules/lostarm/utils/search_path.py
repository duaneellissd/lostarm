import os
from lostarm.utils.verbose_print import VerbosePrint

class SearchPath( VerbosePrint ):
    """
    This helps finding "include files" in a template engine.
    If the file is not found it is a fatal error.
    It is not a FileNotFoundError exception. (that is python vomit)
    we want a user IDE friendly error message instead.
    """
    def __init__(self):
        VerbosePrint.__init__(self)
        self._search_dirs = []

    def add_search_dir(self, path : str ) -> None:
        if not os.path.isdir(path):
            tmp = VerbosePrint()
            tmp.fatal("%s: no such directory" % path )
        self._search_dirs.append(path)

    def find_relative_to(self, filename : str, base_filename : str ) -> str:
        """
        Find this filename.
        It could be an absolute path or relative to the current base_filename.
            The task is FATAL if the specified filename is ABSOLUTE
        it could be a relative path
            It can be relative to the current base_filename.
            Or it can be found in the search path.

        If not found this calls fatal().
        This does not raise an exception, the parser cannot find an include file.
        """
        tried = []
        if os.path.isabs(filename):
            if not os.path.isfile( filename ):
                self.fatal("%s: No such file or directory" % filename )
            return filename
        dn = os.path.dirname( base_filename )
        fn = os.path.join( dn, filename )
        if os.path.isfile(fn):
            # Found!
            return fn
        tried.append(fn)
        for dn in self._search_dirs:
            fn = os.path.join( dn, filename )
            if os.path.isfile(fn):
                # Found!
                return fn
            tried.append(fn)
        # We hit here we cannot find it.
        self.verbose_print(0,"Cannot find filename: %s" % filename)
        for n, name in enumerate(tried):
            self.verbose_print(0,"%2d) %s" % (n,name) )
        self.fatal("Cannot find filename: %s" % filename)
        return "" # dummy to shut up pylance
