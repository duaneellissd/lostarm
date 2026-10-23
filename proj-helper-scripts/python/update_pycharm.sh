def my_which( name ):
    path = os.environ.get( 'PATH' )
    path_list = path.split( os.pathsep )
    tried = []
    for this_dir in path_list:
        tmp = os.path.join( this_dir, name )
        if os.path.isfile( tmp ):
            return tmp
        tried.append( tmp )
    print("FATAL: Cannot find: %s" % name )
    for n, tmp in enumerate( tried ):
        print ("Tried: %2d) %s" % (n,tmp)
    sys.exit(1)
    
# has the user specified where PYCHARM is located?
PROJ_PYCHARM_EXE = os.environ.get("PROJ_PYCHARM_EXE", None)
