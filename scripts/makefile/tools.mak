# -*- mode: makefile -*-

TARGET_compiler_flavor=gcc

TARGET_AS = $(CROSS_COMPILE)as
TARGET_CC = $(CROSS_COMPILE)gcc
TARGET_CXX = $(CROSS_COMPILE)g++
TARGET_GDB = $(CROSS_COMPILE)gdb
TARGET_LD = $(CROSS_COMPILE)ld
TARGET_OBJCOPY = $(CROSS_COMPILE)objcopy
TARGET_OBJDUMP = $(CROSS_COMPILE)objdump
TARGET_SIZE = $(CROSS_COMPILE)size
TARGET_STRIP = $(CROSS_COMPILE)strip
TARGET_AR = $(CROSS_COMPILE)ar

HOST_compiler_flavor=gcc
HOST_AS = as
HOST_CC = gcc
HOST_CXX = g++
HOST_GDB = gdb
HOST_LD = ld
HOST_OBJCOPY = objcopy
HOST_OBJDUMP = objdump
HOST_SIZE = size
HOST_STRIP = strip
HOST_AR = ar

RM = rm
ECHO = @echo
CP = cp
MKDIR = mkdir
MKDIR_P = mkdir -p
SED = sed
CAT = cat
TOUCH = touch
PYTHON3 = python3

CLANG_WARNINGS = -Wextra-tokens -Wdeprecated
