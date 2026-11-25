# This is all about how this PROJECT uses Python

## To define some variables

The variable: PROJ_ROOT_DIR is the top most directory in the project,
it is where your top most ".git" directory is located.  

There are many other Env Variables, they are described here:

    `${PROJ_ROOT_DIR}/docs/ENV_VARS.md`

### **`PROJ_PYTHON_EXE`**

0. Note specifically, the variable contains the digit 3, we want Python Version 3 something, not Python Version 2.
1. This package uses python extensively. And there are various problems with PYTHON in your path. (Described below).
2. Thus we do not (on purpose) use the PYTHON application from your path (Reasons are described below). This must always resolve to an executable file that is Python.
3. On a windows platform that means: `python.exe`
4. On Linux/Mac it is the 'python' you wish to use, in some cases it might be a shell script that undoes the nastiness forced upon you by various IDEs you might be using (Described below in more detail).

Note for Windows users:

Of the bastards at Microsoft place installs in the location:
"c:\progam files\python311" or something like that.

that space in there is a nasty problem.

If you have installed Python in that directory, then you must do
something extra.

In Windows, you must define PROJ_PYTHON_EXE="c:\program files\python315" Note the double quotes here.

Once you have set this, you must do a test.

STEP 1 - Open a command prompt.

STEP 2 - Type  %PROJ_PYTHON_EXE% --version

This should work and print the verison of your python install.  If you
get an error you probably need to fix the quotes so the
"program<space>files" work.


### **`PROJ_PYTHON_DIR`**

1. Most often this is `${PROJ_ROOT_DIR}/helper-scripts/python`
2. There are various internal "python modules" that we do not install, and other python things.
3. Why? They are not ready for 'pypy' and they work as a package, for now it is easier this way.
3. All of these things are stored in that directory.
4. These modules can be found here `${PROJ_PYTHON_DIR}/modules`

### **`PROJ_VENV_DIR`**

1. Most often it is: `${PROJ_ROOT_DIR}/.venv`
2. This is where we will create and use our Python Virtual Environment.
3. You should also know about the

## This sounds stupid, why are you doing this?

### Welcome to DLL HELL

At this point in Pythons life it has reached the old "DLL HELL"
problem that early Microsoft Windows users had/have.

Details here: [DLL HELL](https://en.wikipedia.org/wiki/DLL_hell)
Also here: [DEPENDENCY HELL](https://en.wikipedia.org/wiki/Dependency_hell)

Numerous engineering tools now offer Python Support. Most often, the tool has some scheme to provide a loadable binary Python Module. And that is the problem.

### Historically Python did not have a strong and stable Binary API

Part 1: Python generally does not have a stable binary API at the C language interface level.

Details here: [Python C ABI](https://docs.python.org/3/c-api/stable.html)

Part 2: Each tool vendor that embeds Python support must (1) choose some specific python release to use, and (2) That vendor also chooses a release schedule or cadence for the next version or release of their tooling.

Part 3: With 5 different vendors, you have 10 different answers.

**Question:** Do you think they will all agree? If one of those vendors did not do the right thing, who is going to figure out the work around? And does that mean with 5 vendors you quite possibly need 5 different workarounds?

## Reality raises its ugly head and says Hello

**I do not have time for that** nor do you. I need a solution that I can force to work in an easy way across all vendors. This approach has worked well for the last 8-10 years so I am sticking with it. Perhaps you have a better solution, I'd love a better solution that works uniformly across all IDEs that I want to support.

## How many versions of Python do I have/face today?

And they are all incompatible with each other. My hosts are: x86 MACBOOK, Ubuntu Linux (VM on my MACBOOK), Win11 (VM On my MACBOOK), Physical x86 UBUNTU Linux Box (runs my CI/CD jobs)

### As of this writing

1. Today is: 7-sep-2026
2. Python 3.15orc2 is scheduled for 1-oct-2026

### My MACBOOK has

1. /Library/Python/2.7
2. /Library/Python/3.7
3. /Library/Python/3.9
4. /Applications/ti/ccs2002/.../python3

### Linux Has

1. The system version of Python.
2. The Xilinx tools have their private version of Python (V3.8)
3. The Microchip/MicroSemi has its private version of Python.

### Windows

1. Newer versions of Excel support Python, I wonder what version?
2. I have a separate general install of Python 3.12
3. The windows version of Xilinx
4. The Windows version of Microchip/MicroSemi SoftConsole
5. TI Code Composer Studio
6. Standalone Eclipse CDT setup with arm-none-eabi (with Python GDB)

So - 13 different Python variants, this is going to be fun.

You probably need exactly one combination and don't care about the other 12

## What other vendors do

Often vendors solve this by including a private copy of Python with the tool you downloaded. They can sometimes support that version and nothing else.

If you want to use something else you are on your own. We need to take the same approach.

We do not want to perform **surgery** on each of these Tool Chains, we do not have enough bandwidth to support every possible combination and permutation.

## BUT that is what a PYTHON VENV was designed for

Exactly. The way PYTHON VENV works is by way of SHELL Environment variables and it works great.

Then you launch the vendors tool (sometimes via a helper script) and that script will change all of these ENV variables. For example it changes the PATH variable to put their version of Python at the front of the line. The IDE then launches some pre/post build script and nothing works any more.

Hence, our scripts do not use PYTHON in your PATH and instead make use of `${PROJ_PYTHON_EXE}` to launch python.

## Our solution is in several parts

### PART 1 - Avoid the PATH

DO NOT Ever use the `PATH` version of PYTHON. In stead, we require a UNIQUE variable `PROJ_PYTHON_EXE`. This must exist and point to the version of python to use. If it does not exist, we die with a nasty error.

Do not issue Warnings, DIE with a HUMAN useful error message.

### Part 2 - We assume a basic PYTHON 3 level standard library only, avoid Modules

Some of us work in environments where getting things installed is a giant ordeal. A wise man
once told me:

>> The requirement costs to ante up with Classified Poker is not cheap, but the jack pot is huge", and they are paying for that requirement, so let them pay.

That generally reflects on some of the security requirements and thus cost problems with the US Defense programs.

### Part 2 - No PYTHON VOMIT

The PYTHONIC way is often to raise an exception and let it die or exit if the exception is not caught. That is acceptable in some places, and is not acceptable in other places.

Our view: A Python Exception is a lot like a seg-fault, with a stack trace.  

When your C++ compiler finds an error and must bail out, do you expect the TOOL to seg-fault with a stack trace? Or do you expect a usable and human friendly error message.

As one example: This tool uses human edited JSON files to configure things. How many typos do you think will occur or be created as you tweak and use this TOOL? We know that answer is every day, all day, always.

If Python VOMIT occurs it must only occur where there is a true internal error that was not expected. But general everyday errors a normal developer might cause/create **SHALL-NOT-EVER** produce PYTHON VOMIT.

This is important because often some NCG (New College Grad, or wet-behind-the-ears Engineer) has no clue how to figure out if the problem is (A) some python error or (B) their own syntax error. And remember that very senior engineer with 40+ years of experience looking at your complex tool (This very tool) is effectively a NCG.

### Part 3 - To Paraphrase SHAKESPEARE: to VOMIT or not to VOMIT that is the question

Today, many of use use an IDE with a mouse, or a text based tool (Like VIM) and can turn on error plugins. With that plugin in you can select the error and go directly to the offending file.

1. OPTION 1 Should the error link take you deep within the bowels of a PYTHON MODULE?
2. OPTION 2 Take me to the source code file with the issue?

We choose Option 2.

### Part 4 our `${PROJ_PYTHON_VENV_DIR}`

Yes, we do create our own PYTHON Virtual Environment.

We do install a few HELPFUL Python Modules via PIP, but only a few.

More later.

### Part 5 Our own Python Modules

We have developed some of our own Python Modules, but they are not yet "PIP installable" and probably will never become part of PyPy - because they are so specific to this domain problem and are not general purpose.

BUT yet, we wish to use these as a module.

1. Option 1 - We install our modules into our VENV dir.
2. Option 2 - We do not install our modules into our VENV dir.

**Today:** This is also a new/young tool - and we are always adding, improving, extending our internal modules. We do that from within our IDE, we let the IDE debugger step into the module source code.

Installing our module into the VENV is possible, and as you edit/tweak/improve you are doing so in a COPY of the module.  You must then sync your changes back into the copy in the GIT directory.

So we choose **Option 2** - and tell Python via the env variable `PYTHONPATH` where to find the additional modules.

### Part 6 - The PIP Modules we do use

1. Option 1 - Have PIP to fetch these from the internet in the standard way.

2. Option 2 - Keep a private "cached copy" of the modules in the repo.

We choose Option 2 - but that has some complications to address.

1. Preference #1 - always use WHEEL (WHL) modules they are universal.

2. Preference #2 - Use separate `requirements.txt` files

Many modules have WHL files, some do not.  Python Cryptography and a few others have binary components. So what we actually have and use are 2 different `requirements.txt` files.

1. The Generic: `requirements-generic.txt` and
2. The `requirements-macos.txt` file, and a windows and linux one too.

When we build/create the VENV, we install the generic one first, then we install the host specific one next.

**NOTE:** Another trick is to list the requirements in some install order. If Module C requires B and B requires A, then install A first, then B, then C.

The `requirements.txt` files are located here:

    `${PROJ_PYTHON_DIR}/modules/pip-modules`
    
## Using Other IDEs, Related ENV Vars

What we do not know today as we write this, and as you read this is the following: What IDE are you going to use?  Do you want to understand
our PYTHON work? Or just use it.

other tools:

1. Pycharm - `${PROJ_PYCHARM_EXE}`
2. VS CODE - `${PROJ_VSCODE_EXE}`
3. VisualStudio - `${PROJ_VISUALSTUDIO_EXE}` community edition.

These should resolve to the means to launch your instance of the tool

If these are set, we attempt to create a useful bash shell script to launch the IDE with knowledge of the `${PYTHONPATH}` and the VENV we create.

* `lostarm_pycharm.sh`
* `lostarm_vscode.sh`

