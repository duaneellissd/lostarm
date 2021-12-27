# -*- mode: makefile -*-

ifndef LIB_FRONT_MAK
$(error Did you forget to include the macro: LIB_FRONT_MAK)
endif

include ${MAKEFILE_DIR}/compile.mak

include ${MAKEFILE_DIR}/common_targets.mak

the_lib: ${OBJ_DIR}/${LIB_NAME}

${OBJ_DIR}/${LIB_NAME}: ${ALL_OBJS}
	${AR} cr $@ ${ALL_OBJS}

