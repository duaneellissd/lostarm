import os
# What targets do we support?

supported_targets = [ 'linux', 'stm32h7' ]
# if no target is specified, what do we use?
default_target='linux'

# standard names used in makefiles
# and SCons..
generic_gnu_tools = {
    "CC"    : "gcc",
    "CXX"   : "g++",
    "LD"    : "g++",
    "AR"    : "ar",
    "as"    : "as",
    "STRIP" : "strip",
    "PATH"  : os.environ['PATH']
}

build_dir='build.d'

ARM_PREFIX="/usr/bin/arm-linux-gnueabi-"

HERE=os.path.dirname(__file__)

COMMON_INCLUDE_DIRS=[]
tmp = os.path.join( HERE, 'include' )
print("tmp=%s" % tmp)
COMMON_INCLUDE_DIRS.append(tmp)

# Take the GNU tool list above and create
# a new set of tools with prefix applies
def create_cross( dict_in, prefix ):
    result = dict()
    for k,v in dict_in.items():
        tool_exe_filename = prefix + v
        result[k]=tool_exe_filename
    return result

# Maps
#   
tool_table = {
    "linux"   : generic_gnu_tools,
    "stm32h7" : create_cross( generic_gnu_tools, ARM_PREFIX )
}

include_dir_table = {
    "linux" : [ *COMMON_INCLUDE_DIRS ],
    "stm32h7" : [ *COMMON_INCLUDE_DIRS ]
}

common_gcc_cflags = "-Wall -Wmissing-prototypes -Wstrict-prototypes -ggdb"


cflags_table = {
    "linux" : common_gcc_cflags,
    "stm32h7" : common_gcc_cflags
}

defines_table = {
    "linux" : {
        "LINUX" : 1,
        "LOSTARM_CROSS" : 0
        },
    "stm32h7" : {
        "LINUX" : 0,
        "STM32" : 1,
        "LOSTARM_CROSS" : 1 }
}


# Local Variables:
# mode: python
# End:
