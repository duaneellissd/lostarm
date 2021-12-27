# -*- mode: Makefile;  -*-

OBJ_DIR_ROOT=objs

# Deterine multilib...
_MULTI_LIB_DIR := $(shell ${TARGET_CC} ${TARGET_CFLAGS} ${_MULTILIBOPTION} -print-multi-directory)
ifeq ("${_MULTI_LIB_DIR}",".")
MULTI_LIB_DIR  :=
OBJ_DIR        := ${OBJ_DIR_ROOT}/${GNU_TARGET}
else
MULTI_LIB_DIR  := ${_MULTI_LIB_DIR}
OBJ_DIR        := ${OBJ_DIR_ROOT}/${GNU_TARGET}/${_MULTI_LIB_DIR}
endif

HOST_OBJ_DIR   := ${OBJ_DIR_ROOT}/host

MAKE_MULTILIB=${MULTILIB_PL} --gcc='${TARGET_GCC}' --only='${TARGET_MULTILIB_MATCH}'

include ${MAKEFILE_RULES}

# NOTE: I cannot use "${MAKEFLAGS}" here because of cygwin issues.
#       1) Given: On Linux, the command: "make -k"
#       2) This "${MAKE} ${MAKEFLAGS}" resolves to "make k"
#       3) Solution: ${MAKE} ${MAKEFLAGS:%=-%} - works on linux.
#       4) FAILS on cygwin, as MAKEFLAGS contains "--unix"
#          which then becomes "---unix" (3dash-unix) an error.
#       Sigh... yet another wacky thing we must hold our nose for.
multilib.all::
	${MAKE_MULTILIB} --cmd='${MAKE} lib.all'

multilib.combine: 
	${MAKE_MULTILIB} --cmd='${MAKE} lib.combine'

multilib.install.lib:
	${MAKE_MULTILIB} --cmd='${MAKE} install.lib'

OBJS += ${C_SOURCES:%.c=${OBJ_DIR}/%.o}
OBJS += ${S_SOURCES:%.S=${OBJ_DIR}/%.o}
HOST_OBJS += ${HOST_C_SOURCES:%.c=${HOST_OBJ_DIR}/%.o}
HOST_OBJS += ${HOST_S_SOURCES:%.c=${HOST_OBJ_DIR}/%.o}

lib.all::  ${OBJ_DIR} ${OBJS} 
	${TARGET_AR} qcs ${OBJ_DIR}/${LIBNAME} ${OBJS}

hostlib.all:: ${HOST_OBJ_DIR} ${HOST_OBJS}
	${HOST_AR} qcs ${HOST_OBJ_DIR}/${LIBNAME} ${HOST_OBJS}

host.combine:: ${OBJ_DIR}


define LIBCOMBINE_template
	${HIDE}rm -rf ${1} 
	${HIDE}mkdir -p ${1}
	${HIDE}set -e && \
	HERE=`pwd` && \
	for x in ${2} ; \
	do \
		cd ${1} && \
		echo "Processing: $${x} ..." ; \
		for o in `${3} t $${HERE}/../$${x}/${1}/lib$${x}.a` ; \
		do \
			if [ -f $$o ] ; \
			then \
				echo "ERROR: lib$${x}.a - object: $$o - duplicate name in previous library!\n"; \
				exit 1 ; \
			fi ; \
		done ; \
		${3} x $${HERE}/../$${x}/${1}/lib$${x}.a ;\
		cd $${HERE} ; \
	done
	${HIDE}${3} qcs ${1}/${LIBNAME} ${1}/*.o
endef

lib.combine:: ${OBJ_DIR} 
	$(call LIBCOMBINE_template,${OBJ_DIR},${ALL_LIBS},${TARGET_AR})

hostlib.combine:: ${HOST_OBJ_DIR}
	$(call LIBCOMBINE_template,${HOST_OBJ_DIR},${ALL_HOST_LIBS},${HOST_AR})

clean::
	rm -rf ${OBJ_DIR_ROOT}/*
#
${OBJ_DIR} : 
	mkdir -p $@
#
${HOST_OBJ_DIR}:
	mkdir -p $@

remake: clean default


install:: 

XXinstall.lib::
	mkdir -p ${TARGET_LIB_DIR}
	cp ${OBJ_DIR}/${LIBNAME} ${TARGET_LIB_DIR}

install.lib::
	${HIDE}if [ ! -d ${OBJ_DIR} ] ; then echo "Missing: ${OBJ_DIR}" ; exit 1 ; fi
	${HIDE}set -e ; \
	for x in `cd ${OBJ_DIR} && find . -type f -name '${LIBNAME}' -print | grep -v '${HOST_OBJ_DIR}'` ; \
	do  \
		dname=`dirname $$x` ; \
		mkdir -p ${TARGET_LIB_DIR}/$$dname ; \
		echo "Install ${OBJ_DIR}/$$x" ; \
		echo "     to ${TARGET_LIB_DIR}/$$x" ;\
		cp ${OBJ_DIR}/$$x ${TARGET_LIB_DIR}/$$x ; \
	done 

install.host.lib::
	${HIDE}if [ ! -d ${HOST_OBJ_DIR} ] ; then echo "Missing: ${HOST_OBJ_DIR}" ; exit 1 ; fi
	cp ${HOST_OBJ_DIR}/${LIBNAME} ${HOST_LIB_DIR}

# Things to exclude while doing a "tar-copy-dir" installation.
# Version control subdirs
INSTALL_TAR_EXCLUDES += --exclude='.svn'
INSTALL_TAR_EXCLUDES += --exclude='.cvs'
INSTALL_TAR_EXCLUDES += --exclude='.git'
# Any other wacky '.' files...
INSTALL_TAR_EXCLUDES += --exclude='.[a-zA-Z0-9]*'

# All Emacs backup files
INSTALL_TAR_EXCLUDES += --exclude='*~'
# All Emacs LOCK files
#NSTALL_TAR_EXCLUDES += --exclude='\#*'
# All "BAK" files in any form
INSTALL_TAR_EXCLUDES += --exclude='*.[Bb][Aa][kK]'

install.headers:
	$(HIDE)(cd ../include/. && tar ${INSTALL_TAR_EXCLUDES} --create --file=- .) | \
	   (cd  ${TARGET_INC_DIR}/. && tar xfv -)
	$(HIDE)if [ -d ../include_sys ] ; then \
		(cd ../include_sys/. && tar ${INSTALL_TAR_EXCLUDES} --create --file=- .) | \
		   (cd  ${TARGET_INC_DIR}/. && tar xfv -) ; \
	fi

install.host.headers:
	(cd ../include/. && tar ${INSTALL_TAR_EXCLUDES} --create --file=- .) | \
	   (cd  ${HOST_INC_DIR}/. && tar xfv -)
