# HACKING - Getting Started PYTHON Related & VSCODE

## This is a bit of a passion project

YES, this is an IDE project generator.

Question:

   Why are you bothering with this CMAKE has this solved?

Answer:

   I hate with a passion 'CMAKE', google this phrase: "CMAKE HATE"
   The google ai produces this excellent summary (20-jun-2026)

   You are completely justified in hating CMake; it is arguably
   the most frustrating yet necessary tool in the entire software
   engineering ecosystem. While developers coming from Rust (cargo)
   or JavaScript (npm) expect a clean, declarative package manager,
   CMake feels like a baroque programming language from another planet.

I intend to make a better solution.

## Status - TODAY vrs FUTURE plans

* TODAY - this is about PYTHON & VSCODE
* Over time (future) it will be about C code for the host
* Over time (future) it will be about HOST ONLY CI/CD unit testing.
* Over time (future) it will be about C code for various targets (dev boards)
* If you have a different DEV BOARD and you send me for FREE
* Then I MIGHT (no promises) add it to the list if it looks interesting.
* I can, or others can help you do that if you give us money
* Over time (future) it will be about HIL CI/CD testing.
* HIL means: hardware in the loop, ie: unit testing on hardware.

## The TL;DR - impatient set of instructions

You should read the entire README but some do not.
To better understand, read the entire thing.

To setup the required "Python Virtual ENV" do the following:

1. the command: 'python3' exists in your path.
2. cd to the root of the project.
3. Type ```python3 ./helper-scripts/python/vscode_venv_helper.py  .```
4. This creates a ".venv" directory at the location "."
5. Then launch VSCODE, by typing: 'code .'

## what vscode_venv_helper.py does

### Part 0 - There will be GIT CHURN

   This is frustrating :-( no two ways about it

   Sadly, to make a VENV work within vscode requires modifying
   the ```.vscode/settings.json``` so that it points to the VENV
   and - because we have a group of private python modules
   we must tell pylance about this location:

      ```${PROJ_ROOT_DIR}/helper-scripts/python/modules```

   Why? The location where YOU have things checked out will be
   different then where I have things checked out.

   And thus, whenI run the vscode_env_helper.py my directory
   is inserted into settings.json, and the same when you do this.

   I do not know of a way to put this in a separate vscode file
   and I do not know how to tell git to ignore this type of change.
   if you do please let me know, it is frustrating.

### Part 1 - creating the venv and run pip install -r REQUIREMENTS.txt

* it creates a venv directory in the root of the project.
* In the ./helpers-python directory is a 'requirements-SYSTEM.txt'
* SYSTEM might be: Darwin, Linux or Windows
* This file is processed by "pip install -r FILENAME.txt"
* Why multiple requirements files?

   My day job is in a "closed environment" (no internet connection)
   But this is a "home project" and that rule does not apply at home.
   But it is a habit that I follow with many things that I do.

   In that environment we must hand carry packages into the environment
   on a CD ROM. And binary only packages are very
   SYSTEM specific. A WINDOWS binary package does not work on
   LINUX or DARWIN. So we use: requirements-SYSTEM.txt

### Part 2

* My Editor of choice is Emacs [all hail emacs]
* And the IDE of choice (at home) is VSCODE (it is $zero_cost)
* I want VSCODE to see/understand/and-use my VENV
* So the script also updates/creates the VSCODE settings.json
* And creates a VSCODE launch.json file.
* All sw has no-words that trip Cspell so I add some

## basic concept of the "jproject"?

### Basic statement

In general, one should be able to read a JSON description of
a project and generate an IDE consumable project file.

Give a RICH JSON file - any competent PYTHON developer can
read the JSON (python DICT) and create a generator for their IDE.

### Basic Problem to solve - half arsed IDE projects

That IDE project file should not be a 'half-arsed' project.

The CMAKE lie: CMAKE can create an Eclipse Project

The CMAKE truth: CMAKE creates a makefile that eclipse can consume.
I would rather have a first class IDE project.

Eclipse CDT has two types of projects:

1. This is the preferred thing.

   This is managed make project where Eclipse generates the makefile
   With this type, all of the eclipse features works.

   Example: Right Click GOTO DEFINITION works.
   Example: click on a header file, you cannot goto that header file.

2. This is not preferred.

   Eclipse knows there is a command to "clean", ie: "make clean"
   And a command to "build", ie: "make all"
   And a few more targets but not much else.
   None of the indexing features in Eclipse works.

BUT - that is how CMAKE works. And that sucks.

Same but different problems with Visual Studio and XCode

## Hacking, creating your own generator

### STEP 1 - The Basic Work Flow Load the root project

```python
from lostarm.jproject import Jproject
import json

tool = Jproject()
data = tool.load_root_json_project( "my-cool-project" )
# Remember the project is defined as python dict.
assert( isinstance( data, dict ) )
# We could save it and re-read it later :-)
with open( "dump.json", "wt" ) as f:
    json.dump( data, f )
```

### STEP 2 - Load the JPROJECT JSON or just use the JSON

At this point, one can either:

1. continue from the above, or
2. Load the json from a file

The intent is that everything passes in the python dict.

### Step 3 - Create a makefile [in work]

```python
   
# The first example is to create a UNIX Makefile.

# This is the first one we are creating.
from lostarm.jproject import MakeMaker
make_tool = MakeMaker()
# Optional: You might have Makefile templates you want to use.
make_tool.set_template_dir( "/path/to/extra/templates" )

# use the existing data we have from above
make_tool.add_jproject( data )
# OR - maybe you saved it or modified it
# We can always reload it.
make_tool.load_json_file( "/path/to/above/saved/json/file")

# this wraps the other makefiles, think: recursive makefiles

for proj in make_tool.all_projects():
   make_tool.write_makefile( "/path/to/makefile.%s" % proj.name )
# Now that we have each sub-makefile done this creates a wrapper
make_tool.write_master_makefile( "/path/to/makefile" )
# create a bash script usable for a CI/CD run
make_tool.write_bash_script( "/path/to/build_all.sh")
```

### Step 4 - This is the Visual Studio Plan  [Future]

```python

#This is FUTURE not yet.
from lostarm.jproject import VsStudio2022
visual_studio_tool = VsStudio2022()
visual_studio_tool.add_jproject( data )
visual_studio_tool.set_output_dir( "/some/dir/name" )
print("creating sln-file: %s" % visual_studio_tool.solution_filename )
visual_studio_tool.write_sln_file( )
for proj in visual_studio_tool.all_projects():
   print("creating project: %s, file: %s" % (proj.name,proj.filename))
   visual_studio_tool.write_project_file( proj )
fn = "/path/to/some/script.ps1"
visual_studio_tool.write_powershell_script( fn )
# in your CI/CD system you might do this.
# This would run the VisualStudio build from the command line.
execute_powershell_script( fn )
```

### Step 5 - This is the MAC Xcode Tool [Future]

```python

from lostarm.jproject import XcodeTool
# XCODE has different ways to do this.
# And Google AI says (today: 20-jun-2026)
#==========================================
# However, for most modern multi-project setups, 
# Apple recommends using an Xcode Workspace instead of 
# nesting projects directly inside one another
#==========================================
# current plan is to support the "microsoft visual studio method"
```

### Step 6 - Eclipse based things [Future]

```python

# This is future:
from lostarm.jproject import EclipseTool
tool = EclipseTool()
# Everyone of these are different. 
# DAM you to each of these vendors, DAM YOU!
variant = pickone( "Xilinx", "SoftConsole", "STM32Cube", "TICodeComposer" )
# Probably: Probably Generic EclipseCDT First then STM32Cube, then Xilinx
# Need Generic Eclipse might be the only way to build HOST using Eclipse.
tool.set_variant( variant )
# create the ".project" and ".cproject" files.
tool.write_eclipse_project_files( "/path/to/some/directory" )

```
