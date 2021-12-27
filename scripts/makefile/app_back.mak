# -*- mode: makefile -*-

ifndef APP_FRONT_MAK
$(error did you forget to include app_front.mak?, macro: APP_START}
endif

XXX=YeaBaby
include ${MAKEFILE_DIR}/compile.mak

include ${MAKEFILE_DIR}/common_targets.mak

the_app: ${OBJ_DIR}/${APP_NAME}

APP_NAME_EXE := ${OBJ_DIR}/${APP_NAME}${exeext}

${APP_NAME_EXE}: ${ALL_OBJS} ${APP_LIBS}
	${CXX} -g -o $@ ${ALL_OBJS} ${APP_LIBS}


