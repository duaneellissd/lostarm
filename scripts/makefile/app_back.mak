# -*- mode: makefile -*-
#========================================
# PURPOSE:
#   The APPLICATION makefile is split into 2 parts.
#   The "front portion" - and the "back" portion.
#
# This is the backend of the MAKEFILE
#
# As input, we should have already included app_front.mak
ifndef APP_FRONT_MAK
$(error did you forget to include app_front.mak?, macro: APP_FRONT_MAK)
endif

# We should also have the <various>_SOURCES defined (by the parent makefile)
#
# The parent makefile should have defined the application name.
ifndef TARGET_APP_NAME_EXE
$(error TARGET_APP_NAME_EXE should be defined as the application output file)
endif

include ${MAKEFILE_DIR}/compile.${TARGET_compiler_flavor}.target.mak
include ${MAKEFILE_DIR}/compile.${HOST_compiler_flavor}.host.mak

include ${MAKEFILE_DIR}/common_targets.mak

target_app: ${TARGET_OBJ_DIR}/${APP_NAME}
host_app: ${HOST_OBJ_DIR}/${APP_NAME}

TARGET_APP_NAME_EXE := ${TARGET_OBJ_DIR}/${APP_NAME}${exeext}
HOST_APP_NAME_EXE   := ${HOST_OBJ_DIR}/${APP_NAME}${exeext}

${TARGET_APP_NAME_EXE}: target_app_pre ${TARGET_ALL_OBJS}  target_app_post
	${CXX} -g -o $@ ${TARGET_ALL_OBJS} -L ${TARGET_LIB_DIR} ${TARGET_APP_LIBS:%=-l%}

target_app_pre::
	@# This target exists so you can create your own pre/post process
	@# operation prior to linking an application.
target_app_post::
	@# This target exists so you can create your own pre/post process
	@# operation prior to linking an application.


${HOST_APP_NAME_EXE}: host_app_pre ${HOST_ALL_OBJS}  host_app_post
	${CXX} -g -o $@ ${HOST_ALL_OBJS} -L ${HOST_LIB_DIR} ${HOST_APP_LIBS:%=-l%}

host_app_pre::
	@# This target exists so you can create your own pre/post process
	@# operation prior to linking an application.
host_app_post::
	@# This target exists so you can create your own pre/post process
	@# operation prior to linking an application.
