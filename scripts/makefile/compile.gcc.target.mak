# -*- mode: makefile -*-

ifndef BUILD_SUBDIR_NAME
$(error BUILD_SUBDIR_NAME is not defined)
endif

TARGET_OBJ_DIR :=$(BUILD_DIR)/target/$(BUILD_SUBDIR_NAME)

$(TARGET_OBJ_DIR):
	$(HIDE)mkdir -p $(@)


TARGET_C_OBJS   += $(C_SOURCES:%.c=$(TARGET_OBJ_DIR)/%.o)
TARGET_CXX_OBJS += $(CXX_SOURCES:%.c=$(TARGET_OBJ_DIR)/%.o)
TARGET_AS_OBJS  += $(AS_SOURCES:%.S=$(TARGET_OBJ_DIR)/%.o)

TARGET_ALL_OBJS := $(TARGET_EXTRA_OBJS) $(TARGET_C_OBJS) $(TARGET_CXX_OBJS) $(TARGET_AS_OBJS)

TARGET_CFLAGS := $(TARGET_EXTRA_CFLAGS) -g $(ALL_DEFINES:%=-D%) $(ALL_INCLUDE_DIRS:%=-I%)

TARGET_CXXFLAGS := $(TARGET_EXTRA_CXXFLAGS) -g $(ALL_DEFINES) $(ALL_INCLUDE_DIRS:%=-I%)

TARGET_COMPILE.c   := $(TARGET_CC) $(TARGET_CFLAGS)
TARGET_COMPILE.cxx := $(TARGET_CXX) $(TARGET_CXXFLAGS)

TARGET_GCC_DEPFLAGS := -MT ${TARGET_OBJ_DIR}/${*}.o -MMD -MP -MF $(TARGET_OBJ_DIR)/${*}.d

$(TARGET_OBJ_DIR)/%.o: %.c
	${ECHO} "Compile(-c-target): ${*}.c" 
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS} ${TARGET_CFLAGS} -c -o $@ $<

$(TARGET_OBJ_DIR)/%.o: %.cpp
	@${ECHO} "Compile(-c-target): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS}  ${TARGET_CFLAGS} -c -o $@ $<

$(TARGET_OBJ_DIR)/%.s: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS}  ${TARGET_ASFLAGS} -S -o $@ $<

$(TARGET_OBJ_DIR)/%.s: %.cpp
	@${ECHO} "Compile(-S): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS} $(TARGET_CXXFLAGS) -S -o $@ $<

$(TARGET_OBJ_DIR)/%.i: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS} $(TARGET_CFLAGS) -E -o $@ $<

$(TARGET_OBJ_DIR)/%.i: %.cpp
	@${ECHO} "Compile(-E): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS} $(TARGET_CXXFLAGS) -E -o $@ $<

-include $(TARGET_OBJ_DIR)/*.d

%.i_target: $(TARGET_OBJ_DIR)/%.i


