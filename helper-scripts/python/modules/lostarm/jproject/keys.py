class KEYS():
    ENV_VARS = 'ENV_VARS'
    VARS = "VARS"
    MAKE_VARS = 'MAKEFILE_VARS'
    SRC_FILENAMES = 'SRC_FILENAMES'
    INC_FILENAMES = 'INC_FILENAMES'
    SRC_DIRS='SRC_DIRS'
    PROJ_ROOT_DIR='PROJ_ROOT_DIR'
    PROJ_TYPE='PROJ_TYPE'
    CMDLINE_INC_DIRS='CMDLINE_INC_DIRS'
    LINKER_SCRIPT='LINKER_SCRIPT'
    NONE='none'
    JSON_INCLUDE="json_include"
    PRE_BUILD_SCRIPT="/dev/null"
    POST_BUILD_SCRIPT="/dev/null"
    
    # Command Line source/include dir keys.
    CLSID_path="path"
    CLSID_is_include = "is_include"
    CLSID_exclude_pattern = "exclude_pattern"
    CLSID_include_pattern = "include_pattern"
    
    STR_app="app"
    STRS_libs= [ "lib", "lib-static", "lib-shared" ]
    STRS_app_or_libs=[ STR_app, *STRS_libs ]
    

class Jproject_KeyNames:
    KEY_PROJ_TYPE = "TYPE"
    KEY_VARS = "VARS"
    KEY_INC_DIRS = "INC_DIRS"

class RANDOM_KEYS:
    PROJ_TYPE_APP = "app"
    PROJ_TYPE_LIB = "lib"
    PROJ_TYPE_SHARED_LIB = "shared-lib"
    PROJ_TYPE_DLL = PROJ_TYPE_LIB

class Jproject_RequiredVars:
    VAR_APP_NAME = "APP_NAME"
    VAR_APP_VERSION = "APP_VERSION"
    PROJ_ROOT_DIR = "PROJ_ROOT_DIR"

class Jproject_OptVars:
    """
    Gcc option: --include
    """
    VAR_FORCE_INCLUDE="FORCE_INCLUDE"
    """
    Well Known GCC naming convention here.
    """
    C_VERSION="C_VERSION"
    """
    Well known GCC naming convention here.
    """
    CXX_VERSION="CXX_VERSION"
    """
    # These are very compiler specific.
    ie: -m32 or -m64 for x86 gcc
    ie: -mcpu=cortexm3 .. very
    """
    CFLAGS_CPU="CFLAGS_CPU"
    CXXFLAGS_CPU="CXXFLAGS_CPU"
    """
    Random things we forgot abut
    """
    CFLAGS_OTHER="CFLAGS_OTHER"
    CXXFLAGS_OTHER="CXXFLAGS_OTHER"
    """
    CFLAGS is what ever you put here.
    Plus all of the other FLAGS above.
    """
    CFLAGS = "CFLAGS"
    """
    Linker script (often used for embedded platforms)
    Rarely used for host builds
    """
    LINKER_SCRIPT="LINKER_SCRIPT"
    """
    Used for C++ builds. Same rules as CFLAGS.
    """
    CXXFLAGS = "CXXFLAGS"
    """
    Linker flags are what ever you put here
    PLUS the LIBDIRS as per compiler method
    """
    LDFLAGS = "LDFLAGS"

class Jproject_DumpKeyNames:
    KEY_PROJ_TYPE = "TYPE",
    KEY_VARS = "VARS",
    KEY_INC_FILES = "INC_FILES",
    KEY_SRC_FILES = "SRC_FILES",