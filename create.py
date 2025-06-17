import os
import sys

from pmake import main

if __name__ == '__main__':
    args = [ sys.argv[0], '-D', 'PROJ_ROOT_DIR=%s' % os.path.dirname(__file__), 'project.json' ]
    main( args )

    
