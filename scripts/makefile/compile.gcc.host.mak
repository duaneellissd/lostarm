# -*- mode: makefile -*-

ifndef BUILD_SUBDIR_NAME
$(error BUILD_SUBDIR_NAME is not defined)
endif

HOST_OBJ_DIR   :=$(BUILD_DIR)/host/$(BUILD_SUBDIR_NAME)


$(HOST_OBJ_DIR):
	$(HIDE)mkdir -p $(@)


HOST_C_OBJS   += $(C_SOURCES:%.c=$(HOST_OBJ_DIR)/%.o)
HOST_CXX_OBJS += $(CXX_SOURCES:%.c=$(HOST_OBJ_DIR)/%.o)
HOST_AS_OBJS  += $(AS_SOURCES:%.S=$(HOST_OBJ_DIR)/%.o)

HOST_ALL_OBJS := $(HOST_EXTRA_OBJS) $(HOST_C_OBJS) $(HOST_CXX_OBJS) $(HOST_AS_OBJS)

HOST_CFLAGS := $(HOST_EXTRA_CFLAGS) -g $(ALL_DEFINES:%=-D%) $(ALL_INCLUDE_DIRS:%=-I%)

HOST_CXXFLAGS := $(HOST_EXTRA_CXXFLAGS) -g $(ALL_DEFINES) $(ALL_INCLUDE_DIRS:%=-I%)

HOST_COMPILE.c   := $(HOST_CC) $(HOST_CFLAGS)
HOST_COMPILE.cxx := $(HOST_CXX) $(HOST_CXXFLAGS)

HOST_GCC_DEPFLAGS := -MT ${HOST_OBJ_DIR}/${*}.o -MMD -MP -MF $(HOST_OBJ_DIR)/${*}.d


$(HOST_OBJ_DIR)/%.o: %.c
	@${ECHO} "Compile(-c-host): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -c -o $@ $<

$(HOST_OBJ_DIR)/%.o: %.cpp
	@${ECHO} "Compile(-cpp-host): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -c -o $@ $<

$(HOST_OBJ_DIR)/%.s: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_ASFLAGS) -S -o $@ $<

$(HOST_OBJ_DIR)/%.s: %.cpp
	@${ECHO} "Compile(-S): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CXXFLAGS) -S -o $@ $<

$(HOST_OBJ_DIR)/%.i: %.c
	@${ECHO} "Compile(-S): ${*}.c"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.c) ${HOST_GCC_DEPFLAGS} $(HOST_CFLAGS) -E -o $@ $<

$(HOST_OBJ_DIR)/%.i: %.cpp
	@${ECHO} "Compile(-E): ${*}.cpp"
	${HIDE}${MKDIR_P} ${dir $@}
	$(HIDE)$(HOST_COMPILE.cxx) ${HOST_GCC_DEPFLAGS} $(HOST_CXXFLAGS) -E -o $@ $<

-include $(HOST_OBJ_DIR)/*.d

%.i_host: ${HOST_OBJ_DIR}/%.i


