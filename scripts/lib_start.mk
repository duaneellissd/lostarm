OBJS += $(C_SOURCES:%.c=${OBJ_DIR}/*.o)
OBJS += $(CXX_SOURCES:%.cpp=${OBJ_DIR}/*.o)
OBJS += $(AS_SOURCES:%.S=${OBJ_DIR}/*.o)
OBJS += $(AS_SOURCES:%.s=${OBJ_DIR}/*.o)
