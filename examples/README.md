# What are these directories.

Today (17-june-2026) these are just simple examples inside of "makemaker"
that we use to demonstrate the build tool.

FUTURE (when, I do not know yet) they will live in their own git repo

Each thing is defined by a JSON File in the top level of that things directory.

For example:

     1) An APP directory, examples include:
     	   app-hello-world
	   app-usb-serial
	   app-freertos-blinky
	   
     2) The "liblostarm" directory
           This defines 99% of the common things.

     3) A "hal" layer that is board specific.
     	The general directory names are: lib<BOARDNAME>

	   Example: liblinux        is a linux emulation layer.
	   Example: libvs-windows - is a windows Visual Studio emulation layer
           Example: libnucelo-stm32f103 - is a popular nucelo board
	   Example: libti-cc1350-launchpad is for a TI launch pad
	   Example: libdigitlent-arty-s7  is a RISCV fpga based project
	   Example: libpynq-z1-ps	  is for a PYNQ board using the PS section.

Thus in the list provided above we have:
     (3 apps) times (1 common) times (6 target boards) or 18 permuations.

I'm not creating 18 permiations of top level projects.
Instead, via python, the build_all.py script will:
	 a) Create a top level directory: build.d
	 b) Then create these permuations in a simple way
	 