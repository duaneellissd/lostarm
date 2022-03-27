# -*- mode: makefile -*-

ifndef BUILD_SUBDIR_NAME
$(error BUILD_SUBDIR_NAME is not defined)
endif

TARGET_OBJ_DIR :=$(BUILD_DIR)/target/$(BUILD_SUBDIR_NAME)
HOST_OBJ_DIR   :=$(BUILD_DIR)/host/$(BUILD_SUBDIR_NAME)


$(TARGET_OBJ_DIR):
	$(HIDE)mkdir -p $(@)

$(HOST_OBJ_DIR):
	$(HIDE)mkdir -p $(@)


TARGET_C_OBJS   += $(C_SOURCES:%.c=$(TARGET_OBJ_DIR)/%.o)
TARGET_CXX_OBJS += $(CXX_SOURCES:%.c=$(TARGET_OBJ_DIR)/%.o)
TARGET_AS_OBJS  += $(AS_SOURCES:%.S=$(TARGET_OBJ_DIR)/%.o)

HOST_C_OBJS   += $(C_SOURCES:%.c=$(HOST_OBJ_DIR)/%.o)
HOST_CXX_OBJS += $(CXX_SOURCES:%.c=$(HOST_OBJ_DIR)/%.o)
HOST_AS_OBJS  += $(AS_SOURCES:%.S=$(HOST_OBJ_DIR)/%.o)

TARGET_ALL_OBJS := $(TARGET_EXTRA_OBJS) $(TARGET_C_OBJS) $(TARGET_CXX_OBJS) $(TARGET_AS_OBJS)

$(info TARGET_OBJ_DIR $(TARGET_OBJ_DIR))
$(info C_SOURCES $(C_SOURCES))
$(info TARGET_ALL_OBJS $(TARGET_ALL_OBJS))
$(info TARGET_CXX_OBJS $(TARGET_CXX_OBJS))
$(info TARGET_AS_OBJS  $(TARGET_AS_OBJS))

HOST_ALL_OBJS := $(HOST_EXTRA_OBJS) $(HOST_C_OBJS) $(HOST_CXX_OBJS) $(HOST_AS_OBJS)

TARGET_CFLAGS := $(TARGET_EXTRA_CFLAGS) -g $(ALL_DEFINES:%=-D%) $(ALL_INCLUDE_DIRS:%=-I%)

HOST_CFLAGS := $(HOST_EXTRA_CFLAGS) -g $(ALL_DEFINES:%=-D%) $(ALL_INCLUDE_DIRS:%=-I%)

TARGET_CXXFLAGS := $(TARGET_EXTRA_CXXFLAGS) -g $(ALL_DEFINES) $(ALL_INCLUDE_DIRS:%=-I%)

HOST_CXXFLAGS := $(HOST_EXTRA_CXXFLAGS) -g $(ALL_DEFINES) $(ALL_INCLUDE_DIRS:%=-I%)

TARGET_COMPILE.c   := $(TARGET_CC) $(TARGET_CFLAGS)
TARGET_COMPILE.cxx := $(TARGET_CXX) $(TARGET_CXXFLAGS)

HOST_COMPILE.c   := $(HOST_CC) $(HOST_CFLAGS)
HOST_COMPILE.cxx := $(HOST_CXX) $(HOST_CXXFLAGS)

TARGET_GCC_DEPFLAGS := -MT $@ -MMD -MP -MF $(TARGET_OBJ_DIR)/${*}.d
HOST_GCC_DEPFLAGS :=-MT $@ -MMD -MP -MF $(HOST_OBJ_DIR)/${*}.d

$(TARGET_OBJ_DIR)/%.o: %.c
	${ECHO} "Compile(-c-target): ${*}.c" 
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS} ${TARGET_CFLAGS} -c -o $@ $<

$(TARGET_OBJ_DIR)/%.o: %.cpp
	@${ECHO} "Compile(-c-target): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS}  ${TARGET_CFLAGS} -c -o $@ $<

$(TARGET_OBJ_DIR)/%.s: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS}  ${TARGET_ASFLAGS} -S -o $@ $<

$(TARGET_OBJ_DIR)/%.s: %.cpp
	@${ECHO} "Compile(-S): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS} $(TARGET_CXXFLAGS) -S -o $@ $<

$(TARGET_OBJ_DIR)/%.i: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.c) ${TARGET_GCC_DEPFLAGS} $(TARGET_CFLAGS) -E -o $@ $<

$(TARGET_OBJ_DIR)/%.i: %.cpp
	@${ECHO} "Compile(-E): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(TARGET_COMPILE.cxx) ${TARGET_GCC_DEPFLAGS} $(TARGET_CXXFLAGS) -E -o $@ $<

-include $(TARGET_OBJ_DIR)/*.d

$(HOST_OBJ_DIR)/%.o: %.c
	@${ECHO} "Compile(-c-host): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -c -o $@ $<

$(HOST_OBJ_DIR)/%.o: %.cpp
	@${ECHO} "Compile(-cpp-host): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -c -o $@ $<

$(HOST_OBJ_DIR)/%.s: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_ASFLAGS) -S -o $@ $<

$(HOST_OBJ_DIR)/%.s: %.cpp
	@${ECHO} "Compile(-S): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CXXFLAGS) -S -o $@ $<

$(HOST_OBJ_DIR)/%.i: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -E -o $@ $<

$(HOST_OBJ_DIR)/%.i: %.cpp
	@${ECHO} "Compile(-E): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CXXFLAGS) -E -o $@ $<

-include $(HOST_OBJ_DIR)/*.d

%.i_target: $(TARGET_OBJ_DIR)/%.i
%.i_host: ${HOST_OBJ_DIR}/%.i


