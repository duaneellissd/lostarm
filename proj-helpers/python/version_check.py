import sys

def my_print( msg ):
    # We do this incase we are python2.
    sys.stdout.write( msg )
    sys.stdout.write( "\n" )

def fatal( msg ):
    my_print( msg )
    sys.exit(1)


my_print( sys.version )

v = (100 * sys.version_info[0]) + sys.version_info[1]
if v < 310:
    my_print( "this requires python 3.10 or better ")
    # fail.
    sys.exit(1)
else:
    my_print( "python version seems ok")
    # success
    sys.exit(0)
