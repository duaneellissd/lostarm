# Purpose of this directory

If you workin a "closed" environemnt high security enviornment
then the following will be helpful.

a CLOSED environment is closed room with no external connections.
there is no internet connections. But you still need to install things.

To install things one often copies files onto a CDROM
and bring the CDROM into the closed area.

Install the files from the CD, then shred the CDROM

EXTERNAL to the room:
STEP 1	Use 'pip download" to download the packages into a directory.
	example: THIS DIRECTORY.

STEP 2:	Copy this directory structure to a CDROM

STEP 3: Sneakernet the CD into the closed environment.

STEP 4: Copy the CD into/onto that computer.

STEP 5: Remove the CD and shred the CD

STEP 6: you can now install things from this directory.

The install process for the VENV is as follows:

When running "pip install NAME" the process is:
The python helper script does this:

	step 1 - CD to this directory.
	step 2 - run python -m pip install NAME
  	 where NAME is a file in this directory.
	step 3 - CD to old directory

This way you can place copies of your required packages
in this directory

