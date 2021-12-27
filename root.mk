
# This requires GNU Make

PATH:=/opt/local/bin:${PATH}
export PATH

ifndef ROOT_DIR
ROOT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
endif
export ROOT_DIR

ifndef SCRIPTS_DIR
SCRIPTS_DIR := $(ROOT_DIR)/scripts
endif


OBJDIR=${ROOT_DIR}/objs

include ${SCRIPTS_DIR}/names.mk


#----------
# Note: would really like: GNUmakefile
#
# Local Variables:
# mode: Makefile
# End:
