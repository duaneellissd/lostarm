# -*- mode: makefile -*-
RAW_OBJ_DIR := $(shell ${TARGET_CC} ${TARGET_CFLAGS} ${_MULTILIBOPTION} -print-multi-directory)

OBJ_DIR_ROOT := objs

OBJ_DIR      := ${OBJ_DIR_ROOT}/${GNU_TARGET}/${RAW_OBJ_DIR}
HOST_OBJ_DIR := ${OBJ_DIR_ROOT}/host

# must come *after* OBJ_DIR
include ${MAKEFILE_RULES}

app_targets: ${APP_TARGETS:%=${APP_NAME}.%}

host_targets: ${HOST_TARGETS:%=${APP_NAME}.%}

APP_OBJS += ${C_SOURCES:%.c=${OBJ_DIR}/%.o}
APP_OBJS += ${S_SOURCES:%.S=${OBJ_DIR}/%.o}
APP_OBJS += ${BIN_SOURCES:%.bin=${OBJ_DIR}/%.o}

HOST_OBJS += ${HOST_C_SOURCES:%.c=${HOST_OBJ_DIR}/%.o}
HOST_OBJS += ${HOST_BIN_SOURCES:%.bin=${HOST_OBJ_DIR}/%.o}

${OBJ_DIR}:
	mkdir -p $@

clean::
	rm -rf ${OBJ_DIR_ROOT}/*

${HOST_OBJ_DIR}:
	mkdir -p $@

clean::
	rm -rf ${HOST_OBJ_DIR}

${APP_NAME}.target: ${OBJ_DIR} ${APP_OBJS}
	${TARGET_CC} ${TARGET_CFLAGS} ${TARGET_SPECS} -o $@ ${APP_OBJS}

clean::
	rm -rf ${APP_NAME}.target

${APP_NAME}.hostapp: ${APP_NAME}.host

# APP HOST is done in 2 steps..
#   STEP 1 - build & link a temp version.
#   STEP 2 - Create 'host_init.c'
#   STEP 3 - Compile/link link a 2nd time... with host_init.c


${APP_NAME}.host: ${HOST_OBJ_DIR} ${HOST_OBJS}
	${HOST_CC} ${HOST_CFLAGS} -o ${HOST_OBJ_DIR}/tmp_$@ ${HOST_OBJS} -L${HOST_LIB_DIR} -llost
	NM=${HOST_NM} ${HOST_CREATE_INIT_TABLE} ${HOST_OBJ_DIR}/host_init_tab.c ${HOST_OBJ_DIR}/tmp_$@
	${HOST_CC} ${HOST_CFLAGS} -o $@ ${HOST_OBJS} ${HOST_OBJ_DIR}/host_init_tab.c -L${HOST_LIB_DIR} -llost


clean::
	rm -rf ${APP_NAME}.host

${APP_NAME}.size: ${APP_NAME}.target
	${TARGET_SIZE} $< > $@

clean::
	rm -rf ${APP_NAME}.size

${APP_NAME}.symbols: ${APP_NAME}.target
	${TARGET_NM} --demangle --numeric-sort $< > $@

${APP_NAME}.symsize: ${APP_NAME}.target
	${TARGET_NM} --demangle --size-sort $< > $@

clean::
	rm -rf ${APP_NAME}.symbols
	rm -rf ${APP_NAME}.symsize

${APP_NAME}.dis: ${APP_NAME}.target
	${TARGET_OBJDUMP} --line-numbers -d $< > $@

clean::
	rm -rf ${APP_NAME}.dis

${APP_NAME}.rom: ${APP_NAME}.target
	rm -f $@ $@.tmp
	${TARGET_OBJCOPY} -O binary ${APP_NAME}.target $@.tmp
	cat $@.tmp /dev/zero | head --bytes=${TARGET_ROMSIZE} > $@
	rm -f $@.tmp

clean::
	rm -rf ${APP_NAME}.rom

my_gdb:
	rm -f $@ $@.tmp
	echo "#! /bin/sh"                    >> $@.tmp
	echo 'exec ${TARGET_INSIGHT} "$$@"'  >> $@.tmp
	chmod +x $@.tmp
	mv $@.tmp $@

clean::
	rm -rf my_gdb my_gdb.tmp

remake:  clean default