import sys
import os
import time

from projhelpers.utils import DebugHelper

class ExecuteResult(DebugHelper):
    def __init__(self):
        DebugHelper.__init__(self)
        self.exit_code : int = -1
        self.stdout : str = ""
        self.time_start : int = 0 # time.time()
        self.time_end   : int = 0
        # we do not have a stderr
        # REASON: We have stdout and stderr merged into a single output
    
        

class Executor( DebugHelper ):
    def __init__(self):
        DebugHelper.__init__(self)

    def execute_string( self, cmdline_str : str ) -> ExecuteResult:
        return self.execute_args.cmdline_str.split(' ')
    
    def execute_args( self, args : list[str], cwd=None, ignore_exitcode=False, timeout=60 ) -> ExecuteResult:
        """
        args[0] is the executable
        """
        if cwd is None:
            cwd =os.getcwd()
        
        result = ExecuteResult()
        
        self.verbose_print(0,"execute: %s" % " ".join(args))
        # de-quote arg0 incase it is "c:\program files\pythonx.yy\python.exe"
        exe = args[0]
        if exe[0] in ("'",'"'):
            # it is quoted
            if exe[0] != exe[-1]:
                self.fatal("badly quoted executable: %s" % exe )
            args[0] = exe[1:-1]
        result.time_start = time.time()
        py_result = subprocess.run( args,
                                    cwd=cwd,
                                    capture_output=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    timeout=timeout,
                                    check=False, # we do this our self
                                    text=True )
        result.time_end = time.time()
        result.exit_code = py_result.returncode
        result.stdout = py_result.stdout
        # Always provide the output to the human.
        self.verbose_print(0, result.stdout )
        if not ignore_exitcode:
            if result.exit_code != 0:
                self.verbose_print(0,"FAIL: ret code: %d" % result.exitcode )
                sys.exit(result.returncode)
        return result



    
import unittest
import platform

class testExecutor( unittest.TestCase ):
    def create_dut( self ):
        return Executor()
    
    def test_ls(self):
        """
        The test is:  ls OURFILENAME which should always succeed
        """
        # The test case must be different on windows, the "/bin/ls" command does not exist.
        self.assertTrue( platform.system() != 'Windows' )
        args = []
        args.append('/bin/ls')
        tmp = os.path.dirname(os.path.abspath( __file__ ))
        assert( os.path.isfile( tmp ) )
        args.append(temp)
        E = create_dut()
        r = E.execute_args( args )
        self.assertTrue( isinstance( r, ExecuteResult ) )
        self.assertEqual( r.exit_code, 0 )
        tmp = os.path.basename( tmp )
        self.assertTrue( tmp in self.stdout )
        
    

    
