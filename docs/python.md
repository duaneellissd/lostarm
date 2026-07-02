# PYTHON and the env var LOSTARM_PYTHON3_EXE.

## TL;DR - version.

Step 1: We require you have python3.11 or better installed

Step 2: Choose the version (absolute path) to the version of Python3
you wish to use with this project.

WARNING: On Linux this is often not a problem.

WARNING: On Windows.. Grrr...  Please install Python3.11 in
c:\python3.11, or what ever version number you choose. The CRITICAL
item is this: no spaces in the directory path. Example:
"C:\program(SPACE)files\python\blah\blah" <- VERY BAD

WHY? Quoting spaces in scripts is a royal pain in the ass. We have
tried hard to do that correctly, but we obviously could have missed
something.  So the tools will REJECT your choice if it finds a space

Step 3: In your "~/.bashrc" or windows "System ENV settings" create
the env variable: LOSTARM_PYTHON3_EXE and point it to that absolute
path.

Step 4: The script ${PROJ_ROOT_DIR}/create_venv.(sh|bat) will create a
Virtual Environment that things in this tool will need and/or use.

## Why LOSTARM_PYTHON3_EXE

Why is this not just python in your path in some standard way?
Oh I wish it was that easy, but often it is not.

[Some may remember DLL HELL](https://en.wikipedia.org/wiki/DLL_hell)

This problem is very simular. You may not have hit this problem
but I have dam well hit this problem a dozen times or more.

And using a Python Virtual Environment does not solve this problem.

There are some embedded tools that ship with their own private
version of Python, (I'm looking at you Xilinx Vivado and Vitis) And
- Microsemi SoftConsole, and various others...

# Often it is an incompatible version of Python

And you do not have the time to fix that and make that work for you.

* Xilinx might be on an older version of Python
* And Microsemi has yet another version
* And your Linux box has another version.
* And do you need/use GDB with the python extensions?
* And does your IDE require or force that GDB_PYTHON on you?
* And can you change that? or that is really hard and I cannot?
* And what binary version of Python does that GDB require?

Do you have this problem? Probably not, cause you might only have
one of these sets of tools installed.

For me - (I work on very complex systems at the systems level) you are
probably a hobbiest and have exactly 1 thing installed some
others. Due to the nature of my work, I have all of these and perhaps
10 more installed. I deal with this all the time every day.

These tools always insert their version of what ever into your path.
They do not care because their goal is to make their tool work.

Do they do this in a nice way? Or was the python solution in the IDE
tools package put together by pimple faced intern with no clue what or
why they are doing this - they got it to work by hard coding things.

Their view is: To hell with all of the others out there. Their stuff
works only with their version of Python. And you should use their
version of Python to hell with all of your requirements.  They are
your requirements, not THEIR requirements. and they will not support
changing their IDE like that. so go away.

So THANK YOU VERY MUCH you kind &@#$% for thinking about how I can or
cannot use your tools, but I understand you do not care. You shipped
your IDE and I am the 5% case.. you are dealing with the 95% case

And we (you and I) are left holding that bag of dog poop with tools
that do not work, we need a solution.

We require some way to get to the version of python you want to use.
Reguardless of what ever nonsense that tool vendor thrusts upon you.

And it needs to work even if the vendor has changed the PATH variable.

So, we use the variable: LOSTARM_PYTHON3_EXE to find the exact version
of python we want to use in our LOSTARM scripts.

Thus this must be an absolute path and be an Exported ENV Variable.

## OTHER IDES - PyCharm, VSCODE etc.

Next - you probably need to debug your python scripts or you need to
debug the LOSTARM_PYTHON Scripts. You probably want to use a tool like
VSCODE, or PYCHARM - exactly how these tools discover our Virtual
Environment and OUR instance of Python varies.  To that end...
the script ${PROJ_ROOT_DIR}/helper-scripts/python/venv_helper.py
attempts _the best it can_ - to create and setup configuration files
and wrapper scripts that you can use to launch VSCODE and/or PYCHARM
and have it recognize and find the VENV we will create.




