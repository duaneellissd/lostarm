include ../root_settings.mk
_default:build

clean:
	rm -rf html
	rm -rf latex

.PHONY:: clean

build:
	echo PATH=${PATH}
	`which doxygen` lostarm_doxygen_cfg

.PHONY:: build

remake: clean build
.PHONY:: remake
