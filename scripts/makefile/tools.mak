# -*- mode: makefile -*-

AS = $(CROSS_COMPILE)as
CC = $(CROSS_COMPILE)gcc
CXX = $(CROSS_COMPILE)g++
GDB = $(CROSS_COMPILE)gdb
LD = $(CROSS_COMPILE)ld
OBJCOPY = $(CROSS_COMPILE)objcopy
OBJDUMP = $(CROSS_COMPILE)objdump
SIZE = $(CROSS_COMPILE)size
STRIP = $(CROSS_COMPILE)strip
AR = $(CROSS_COMPILE)ar

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
