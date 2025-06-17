import argparse

def parse_args(args):
    ap = argparse.ArgumentParser( prog=args[0] )
    args = args[1:]
    ap.add_argument( "--logfile", dest='log_filename', default="/dev/stdout", help="Log filename")
    ap.add_argument( "-D", dest='vars', action='append', default=[], help='command line defines' )
    ap.add_argument( "ROOT", default=None, help='root project file' )
    return ap.parse_args( args )

