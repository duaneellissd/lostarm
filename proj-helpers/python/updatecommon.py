import os
import sys
import subprocess

def my_which( name ):
    path = os.environ.get('PATH')
    path = path.split(os.pathsep)
    tried = []
    for tmp in path:
        tmp = os.path.join( tmp, name )
        tried.append(tmp)
        if os.path.exists( tmp ):
            return (tmp,[])
    return (None,tried)
        


