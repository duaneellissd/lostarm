# -*- mode: makefile -*-

LIB_FRONT_MAK=true

ifndef LIB_NAME
$(error LIB_NAME is not defined)
endif

ifndef BUILD_SUBDIR_NAME
BUILD_SUBDIR_NAME := ${APP_NAME}
endif

