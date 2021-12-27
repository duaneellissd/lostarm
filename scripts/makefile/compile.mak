# -*- mode: makefile -*-

ifndef BUILD_SUBDIR_NAME
$(error BUILD_SUBDIR_NAME is not defined)
endif

OBJ_DIR :=$(BUILD_DIR)/$(BUILD_SUBDIR_NAME)


$(OBJ_DIR):
	$(HIDE)mkdir -p $(@)


C_OBJS   += $(C_SOURCES:%.c=$(OBJ_DIR)/%.o)
CXX_OBJS += $(CXX_SOURCES:%.c=$(OBJ_DIR)/%.o)
AS_OBJS  += $(AS_SOURCES:%.S=$(OBJ_DIR)/%.o)

ALL_OBJS += $(C_OBJS)
ALL_OBJS += $(CXX_OBJS)
ALL_OBJS += $(AS_OBJS)


CFLAGS += -g 
CFLAGS += $(ALL_DEFINES)
CFLAGS += $(ALL_INCLUDE_DIRS:%=-I%)

CXXFLAGS += -g
CXXFLAGS += $(ALL_DEFINES)
CXXFLAGS += $(ALL_INCLUDE_DIRS)

COMPILE.c   := $(CC) $(CFLAGS)
COMPILE.cxx := $(CXX) $(CXXFLAGS)

$(OBJ_DIR)/%.o: %.c
	@${ECHO} "Compile: ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.c) -c -o $@ $<

$(OBJ_DIR)/%.o: %.cpp
	@${ECHO} "Compile: ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.cxx) -c -o $@ $<

$(OBJ_DIR)/%.s: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.c) -S -o $@ $<

$(OBJ_DIR)/%.s: %.cpp
	@${ECHO} "Compile(-S): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.cxx) -S -o $@ $<

$(OBJ_DIR)/%.i: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.c) -E -o $@ $<

$(OBJ_DIR)/%.i: %.cpp
	@${ECHO} "Compile(-E): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(COMPILE.cxx) -E -o $@ $<

#-import $(OBJ_DIR)/*.d


