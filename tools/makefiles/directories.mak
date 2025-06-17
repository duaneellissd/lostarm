# -*- mode: makefile -*-

ifndef PROJ_ROOT_DIR
export PROJ_ROOT_DIR
$(error Variable: PROJ_ROOT_DIR is not defined)
endif

ifndef BUILD_ROOT_DIR
export BUILD_ROOT_DIR
$(error Variable: BUILD_ROOT_DIR is not defined)
endif

TOOLS_DIR      := ${PROJ_ROOT_DIR}/tools
MAKESCRIPT_DIR := ${TOOLS_DIR}/makefiles

