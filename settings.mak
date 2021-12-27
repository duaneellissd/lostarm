# -*- mode: makefile -*-

ifeq ("$(origin V)", "command line")
BUILD_VERBOSE=$(V)
endif
ifndef BUILD_VERBOSE
BUILD_VERBOSE = 0
endif
ifeq ($(BUILD_VERBOSE),0)
HIDE = @
else
HIDE =
endif
# Since this is a new feature, advertise it
ifeq ($(BUILD_VERBOSE),0)
$(info Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.)
endif

ifndef ROOT_DIR
_SETTINGS_MAK := $(abspath $(lastword $(MAKEFILE_LIST)))
ROOT_DIR := $(shell cd $(dir $(_SETTINGS_MAK)) ; pwd)
export ROOT_DIR
endif

SCRIPTS_DIR   := $(ROOT_DIR)/scripts
BUILD_DIR    := $(ROOT_DIR)/build
MAKEFILE_DIR := $(SCRIPTS_DIR)/makefile

include $(MAKEFILE_DIR)/names.mak
include $(MAKEFILE_DIR)/common_targets.mak
include $(MAKEFILE_DIR)/tools.mak


APP_FRONT_MAK := $(MAKEFILE_DIR)/app_front.mak
APP_BACK_MAK  := $(MAKEFILE_DIR)/app_back.mak

LIB_FRONT_MAK := $(MAKEFILE_DIR)/lib_front.mak
LIB_BACK_MAK  := $(MAKEFILE_DIR)/lib_back.mak

ALL_INCLUDE_DIRS += ${ROOT_DIR}/include
