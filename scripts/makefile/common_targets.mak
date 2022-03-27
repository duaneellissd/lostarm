# -*- mode: makefile -*-

clean::
	rm -rf $(BUILD_DIR)

whatis_%:
	@echo "Variable: $(*) is: $($(*))"

remake: clean _default

all: _default
