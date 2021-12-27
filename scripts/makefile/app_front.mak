# -*- mode: makefile -*-

APP_FRONT_MAK=done
ifndef APP_NAME
$(error APP_NAME is not defined)
endif

ifndef BUILD_SUBDIR_NAME
BUILD_SUBDIR_NAME := ${APP_NAME}
endif

