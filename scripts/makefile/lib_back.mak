# -*- mode: makefile -*-

ifndef LIB_FRONT_MAK
$(error Did you forget to include the macro: LIB_FRONT_MAK)
endif

include ${MAKEFILE_DIR}/compile.${TARGET_compiler_flavor}.target.mak
include ${MAKEFILE_DIR}/compile.${HOST_compiler_flavor}.host.mak

include ${MAKEFILE_DIR}/common_targets.mak

TARGET_LIB_NAME_EXT=${TARGET_OBJ_DIR}/lib${LIB_NAME}${libext}
target_lib: ${TARGET_LIB_NAME_EXT}

HOST_LIB_NAME_EXT=${HOST_OBJ_DIR}/lib${LIB_NAME}${libext}
host_lib: ${HOST_LIB_NAME_EXT}

${TARGET_LIB_NAME_EXT}: lib_pre_target ${TARGET_ALL_OBJS} lib_post_target
	${TARGET_AR} cr $@ ${TARGET_ALL_OBJS}

${HOST_LIB_NAME_EXT}: lib_pre_host ${HOST_ALL_OBJS} lib_post_host
	${HOST_AR} cr $@ ${HOST_ALL_OBJS}

lib_pre_target::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib
lib_post_target::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib

lib_pre_host::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib
lib_post_host::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib


target_install: ${TARGET_LIB_NAME_EXT}
	mkdir -p ${TARGET_LIB_DIR}
	cp ${TARGET_LIB_NAME_EXT} ${TARGET_LIB_DIR}/.

host_install: ${HOST_LIB_NAME_EXT}
	mkdir -p ${HOST_LIB_DIR}
	cp ${HOST_LIB_NAME_EXT} ${HOST_LIB_DIR}/.
