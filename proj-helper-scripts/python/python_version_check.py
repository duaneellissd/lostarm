import sys
import platform

print( "python: %s" % sys.version )

# get it as an integer number
version = (sys.version_info[0] * 100) + sys.version_info[1]
if version < 310:
    print( "python_exe is: %s\n" % sys.executable )
    print( "FATAL: this tool requires python 3.10 or better. Please upgrade\n" )
    sys.exit(1)

print( "SUCCESS: Python version is good\n" )

system=platform.system()
print( "platform: %s" % platform.system() )
if system == "Darwin":
    print("Platform [should be] well supported\n")
elif system == 'Linux':
    print("Platform [should be] well supported\n")
elif system == "Windows":
    print("Platform widnows does not have good test coverage.\n")
    print("Your results may vary...\n")
else:
    print("Hmm. I do not recognize this platform.system()\n")
    print("We can only assume it works...\n")


sys.exit(0)

