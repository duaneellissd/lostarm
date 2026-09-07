# lostarm

## Getting started

## Step 1: Assuming you have done the GIT CLONE

   In this Markdown file, this is known as the `${GIT_CHECKOUT_DIR}`

   This directory is also known as the `${PROJ_ROOT_DIR}`

## There are a lot more Markdown docs located here

   [`${PROJ_ROOT_DIR}/docs`](docs)

## Step 2: Linux/Mac only (for now, future: Windows using GIT BASH)

## Step 3: This tool makes extensive use of Python

Details here: [```${PROJ_ROOT_DIR}/ALL_ABOUT_PYTHON.md```](docs/ALL_ABOUT_PYTHON.md)
  
Yes, we make use of a Python VENV...

Meanwhile: You must set an ENVIRONMENT variable as follows. Typically you would do this in your .bashrc file, then logout log back in.
  
   `export LOSTARM_PYTHON_EXE=/path/to/your/version/of/python`

## Step 4: Open a console and goto the ${PROJ_ROOT_DIR}

1) `bash $_`
2) `cd ${PROJ_ROOT_DIR}`

## Step 5: Make sure you have host build tools installed

Assuming Linux is your host, on Ubuntu:

   1) `sudo apt get update`
   2) `sudo apt install build-essential`

What is required is this:

1) Python, via `LOSTARM_PYTHON_EXE`
2) Complete GCC toolchain, (or clang) for the host
3) GNU Make (We generate Makefile(s))
4) MAC ONLY: xcode - we generate GNU XCode Project files
5) Windows Only: Visual Studio Community Edition (We generate visual studio project files)
6) CROSS Only: We generate various Eclipse Project files.
7) The suggestion is to start with the host, then look at the cross compile features later

## Step 6:  Run the CI/CD Build script

OPTION 1:

   ```bash ./ci_build.sh``` Should build all host unit test things

That script actually just a wrapper around "option 2" below.

## STEP 7: Or build a specific item

OPTION 2:

   To build a specific item, type:

   ```bash ./build.sh --build path/to/projectdir```

   SUGGESTION:  Try this first

   ```bash ./build.sh --build testapps/hostonly_helloworld```

## Step 7: Future - cross compiling

   You may need to setup your cross compiler first
   So skim over this and revisit this later.

   Details here: ${PROJ_ROOT_DIR}/docs/CROSS_COMPILE.md

   1) `bash$ cd ${PROJ_ROOT_DIR}`
   2) `source ./all_settings.sh`
   3) `bash ./build.sh --cross ./cross/TOOLFILE --build path/to/projectdir`

## NOTE: About HOSTONLY and TARGETONLY and GENERIC projects

   While the goal is anything should be anywhere.
   Sometimes some things just do not. This is indicated
   by prefix to the directory name.

   Any project that begins with "hostonly" builds on the host only.

   Any project that begins with "generic" should build anywhere.  But take that with a grain of salt..

   Windows generally does not have a "spi" interface.
   So the spi-test app does not work on that platform.

   BUT the SPI test app does work on Linux, and all embedded platforms.

## STEP 8 Cross Compiling things

   Details are here:

      [`${PROJ_ROOT_DIR}/docs/CROSS_COMPILE.md](docs/CROSS_COMPILE.md)

   And see:
      [`${PROJ_ROOT_DIR}/cross`](cross)

Step 4: bash ./smoke_test.sh (this runs a selftest host only)

## History: Where did this come from?

### History From 20 years ago

Duane Ellis started this 20 years ago (2006/2007) between jobs on Source Forge and did quite a bit of extensive work with OpenOCD at the time. Then Today it lives on GITHUB. Life happened, life got in the way (dad/job things). Other jobs occurred, he moved across country, NJ to CA and recently he picked this back up again.

### Recent Activity

Duane Ellis is also one of the mods for Reddit: r/embedded, and has often needed (wants) a simple embedded target he could use to write some demonstration code to illustrate something.  One day, Duane might actually publish a book or teach embedded sw engineering somewhere

The plan is to use this work as the base.

### Obligatory Money Plug

[shameless plug] Duane Ellis might one day hang a shingle out there and offer consulting services for your company or your project.

### Major Parts

Major parts, and concepts here are things he has learned over his nearly 40 years of Embedded SW Development.

As with history and anything you do, things do not exactly repeat them selves but they sure do rhyme. There is always reuse and re-invention. Thats another important aspect to this.

The things here have existed (been recreated) in just about every previous employers job - but they own those copyrights to those specific private instances developed on their time, on their equipment, for their purposes.  Those instances are their private copies and they own those, along with the patents and products I was part of at those companies.

### The Know How

You hire a senior software engineer because they know how to assemble multiple concepts and parts into a cohesive whole that works.  You cannot own these basic concepts (like a patented idea). Nobody can patent or own the concept of DEBUG_printf(), or a GPIO_wrPin() function.

Nor can they claim the naming convention or writing style, if they could perhaps only the US Author Steven King can write horror books, and only JK Rowling can write wizard books and nobody could paint a vase of flowers again.

Concepts at that level are public. And that is what this is what it intends to be.

### What Platforms did these concepts come from?

Suffice it to say: This is probably the 10th version of this code. It has run on in some form or another, in rough chronological order:

1. An ARM7TDMI
2. A custom 24bit CPU (SNK8)
3. A custom 32bit CPU (SNK32)
4. An ARM9 (rm9200 - Atmel)
5. An ARMv5TE (arm946) custom silicon
6. SunOS - (pre Solaris)
7. NEC V850 CPU
8. Intel Linux
9. TI beagle Bone Black Linux
10. Raspberry PI Linux
11. A RISCV Xilinx Flavor
12. A RISCV Microsemi Flavor
13. Microsemi Flavor CortexM3 (with FPGA)
14. Xilinx Microblaze4 (prior to microblaze 5)

FUTURE Plans are other boards in Duane's box of old eval boards (No specific order, just a list)

* ESP32
* NXP1768 (cortexM3)
* TI CC1350 and CC2652 series (cortexM3)
* Arduino (AVR)
* What ever else duane finds in the 'junk box'
