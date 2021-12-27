

# -*- mode: makefile -*-

# Basic compile a target
${OBJ_DIR}/%.o: %.c
	$(HIDE)${TARGET_CC} ${TARGET_CFLAGS} ${_MULTILIBOPTION} -g -c -o $@ $<

${HOST_OBJ_DIR}/%.o: %.c
	${HOST_CC} ${HOST_CFLAGS} -g -c -o $@ $<


%.i: %.c
	${HIDE}${TARGET_CC} ${TARGET_CFLAGS} ${_MULTILIBOPTION} -g -E -o $@ $<

clean::
	rm -rf *.i

%.ii: %.c
	${HIDE}${TARGET_CC} ${TARGET_CFLAGS} ${_MULTILIBOPTION} -g -E -C -CC -o $@ $<

clean::
	rm -rf *.ii

${OBJ_DIR}/%.o: %.S
	${HIDE}${TARGET_CC} ${TARGET_ASFLAGS} ${_MULTILIBOPTION} -D__ASSEMBLER__ -g -c -o $@ $<

%.i: %.S
	${HIDE}${TARGET_CC} ${TARGET_ASFLAGS} ${_MULTILIBOPTION} -D__ASSEMBLER__ -g -E -o $@ $<

%.ii: %.S
	${HIDE}${TARGET_CC} ${TARGET_ASFLAGS} ${_MULTILIBOPTION} -D__ASSEMBLER__ -g -E -C -CC -o $@ $<

whatis_%: 
	  @echo "${*} = |${${*}}|"

clean::
	rm -f *~

${OBJ_DIR}/%.o: %.bin
	GCC_EXE='${TARGET_CC} ${TARGET_ASFLAGS}' ${BIN2O_PL} -o $@ -s ${<:%.bin=%} $<

${HOST_OBJ_DIR}/%.o: %.bin
	GCC_EXE='${HOST_CC}' ${BIN2O_PL} -l $@ -s  ${<:%.bin=%} $<
