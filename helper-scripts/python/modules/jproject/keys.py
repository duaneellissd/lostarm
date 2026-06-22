class KEYS():
    ENV_VARS = 'ENV_VARS'
    VARS = "VARS"
    MAKE_VARS = 'MAKEFILE_VARS'
    SRC_FILENAMES = 'SRC_FILENAMES'
    INC_FILENAMES = 'INC_FILENAMES'
    SRC_DIRS='SRC_DIRS'
    PROJ_ROOT_DIR='PROJ_ROOT_DIR'
    PROJ_TYPE='TYPE',
    CMDLINE_INC_DIRS='CMDLINE_INC_DIRS'
    LINKER_SCRIPT='LINKER_SCRIPT',
    NONE='none'
    JSON_INCLUDE="json_include",
    PRE_BUILD_SCRIPT="/dev/null",
    POST_BUILD_SCRIPT="/dev/null",

    # Command Line source/include dir keys.
    CLSID_path="path"
    CLSID_isinclude = "is_include"
    CLSID_exclude_pattern = "include_pattern"
    CLSID_include_pattern = "include_pattern"

    STR_app="app"
    STRS_libs= [ "lib", "lib-static", "lib-shared" ]
    STRS_app_or_libs=[ STR_app, *STRS_libs ]