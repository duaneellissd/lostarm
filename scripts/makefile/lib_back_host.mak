# -*- mode: makefile -*-

ifndef LIB_FRONT_MAK
$(error Did you forget to include the macro: LIB_FRONT_MAK)
endif

include ${MAKEFILE_DIR}/compile.mak

include ${MAKEFILE_DIR}/common_targets.mak

HOST_LIB_NAME_EXT=${HOST_OBJ_DIR}/lib${LIB_NAME}${libext}
the_lib: ${LIB_NAME_EXT}

${LIB_NAME_EXT}: lib_pre_target ${HOST_ALL_OBJS} lib_post_target
	${AR} cr $@ ${HOST_ALL_OBJS}

lib_pre_target::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib
lib_post_target::
	@# This target exists so you can create your own pre/post process
	@# operation prior to creating the lib


install: ${LIB_NAME_EXT}
	mkdir -p ${HOST_LIB_DIR}
	cp ${LIB_NAME_EXT} ${HOST_LIB_DIR}/.
