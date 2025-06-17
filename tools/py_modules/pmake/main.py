import os
import pmake
import sys
from pmake.variables import add_cmdline_variable
from pmake.variables import add_builtin_variable


def main( args ):
    print("This code is not ready for prime time (bugs)")
    sys.exit(1)
    args = pmake.parse_args( args )
    pmake.open_log_file( args.log_filename )
    tmp = os.path.abspath( args.ROOT )
    prd = os.path.dirname( tmp )
    add_builtin_variable( 'PROJ_ROOT_DIR', prd )
    for namevalue in args.vars:
        parts = namevalue.split('=',1)
        add_cmdline_variable( parts[0], parts[1] )
    data = pmake.json_wrapper( args.ROOT )
    
