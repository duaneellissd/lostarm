# What is the syntax of a JPROJECT?

First - it is a JSON file.

Every JSON file in the package must have this element, the TYPE sets the other required elements.

```json
    {
        "TYPE" : "some_name"
    }
```

Where: ```some_name``` is one of:

* app - this builds an application.
* lib-static - this builds a static library
* lib-shared - this builds a shared library (linux SO file, or windows DLL)
* multiple - a collection of apps and/or libs, perhaps with some common components.
* In the future we might add more ```"TYPE" : "NAMES"```

Each of the above is described in some more detail, with examples below.

## The main underlying concept going on

This is a very "embedded software" focused tool.

In the embedded world or environment, one does not "install" a package.

Generally the tools (IDEs such as KEIL or IAR) do not provide a means to add a package (library). Nor does Visual Studio support such a thing.

## It's about tailoring the library to the specific product or project.

This is also true of how many embedded projects are built. Often a 'so-called' library is purely rebuilt from source code every time. In the embedded world due to resource constraints, one does not have a prebuilt library. In contrast, on Linux a library is often FULL featured with everything enabled. ie: For OPENSSL, just about all encryption techniques are always present. In contrast, in a resource constrained system - if you are not using BLOWFISH or 2FISH, or SHA1 do you include these as part of the library? That answer is NO.

You might for example receive a preconfigured library but your IDE does not support adding a library with its associated header files. There is no means to "install" something. Instead, you get a source code project that builds either (1) a bunch of C code to object files you link with, or (2) [rare] it actually builds a custom tailored static library.

Case in point: LWIP and FREERTOS - two very popular things. If you need IPV4 only, then you disable IV6 and gain the code space back. In LWIP you might choose 8 not 9 network buffers. So you compile the LWIP code to be exactly that big. The same applies to the FREERTOS configuration. On Linux you might say: everything gets a 1 megabyte stack. But in the embedded resource constrained system, you are counting byte for stack size.

There are so many configuration permutations that it is very impractical to provide a prebuilt library that could be installed.

Instead - what you really have are 3 things:

1. A directory full of "C source files" you need to compile.
2. A directory to add as a "compiler command line include directory"
3. A header file that has all of these configuration #defines.

You want to add that to your IDE project.

And you have 4 more libraries just like that.

On top of that you'll have the following:

1. A directory where your "application code lives"
2. A directory where your "application header files live"
3. Perhaps a configuration header for your application.
4. A linker script that is specific to your chip or your board or app.

For a Linux or windows developer, that linker script is something new to you.
It has always been there, it was just hidden because it was very standardized by
either Microsoft (Windows), Apple (Darwin/MacOS), or Linux(Developers).

## Major JSON Keys every project has

So - to that end - the major items you find in a JPROJECT json file are:

1. The JSON key: "SRC_DIRS"
2. The JSON KEY: "CMDLINE_INC_DIRS"
3. What is called a "FORCE_INCLUDE_FILE"

## What is a "FORCE_INCLUDE_FILE", you might have never heard of it

I first learned of this as a "JAMB FILE" in at the time, the MetroWorks C compiler
The concept is as follows:

1. In your IDE you can add a command line #define
2. But the little tiny window in the IDE GUI to do that sucks.
3. Often you cannot comment out one line or add another in a simple way.
4. The list of #defines can get very long.
5. Its often better to put these in a regular C file
6. And have the compiler ```#include "THATFILE.h"``` for every source file.
7. BUT.. that means modifying every source file to ```#include "THATFILE.h"```
8. Why not tell the C compiler, 'read this file first' then read the real source file.
9. In effect, "jamb this header file in front of each and every source file".

The compiler: gcc (and clang) support this, via the ``--include /path/to/THATFILE.h`` option.
That solves the problem for most LINUX based tools, and DARWIN.

Visual Studio (Windows) supports the same feature with the. ```/FI /path/to/THATFILE.h``` option.

Other tools, like IAR has ```--preinclude /path/to/THATFILE.h".

Depending on the version of KIEL (ARMCC or ARMCLANG) the option is: ```--include``` or ``--preinclude``

## FORCE_INCLUDE limits

These are my rules, my suggestion. Which you are free to ignore.

IMHO (In my humble opinion) a 'force-include' should.

1. ONLY contain comments and #defines and nothing but #defines
2. They shall NEVER ```#include "/some/other/file.h"```
3. They shall never provide a type, or a struct or a global/extern.
4. This is only a replacement for command line #defines only.

The intent is that:

1. Only the APPLICATION shall provide one and only one ```force_include.h```
2. Packages can provide something to merge into the one and only one ```force_include.h``` file.
3. In the GNU world, you often see: 'config.h'
4. A semi-good example of this is the LWIP: "lwipopts.h" 
5. A semi-good example is also: FreeRTOS "FreeRTOSConfig.h"
6. Or the semi-good Azure/ThreadX "tx_user.h" file.

Some are better then others, what I have seen wrong is this:

* Some provide a class, typedef or struct
* Some provide a #define that turns into code, ie: ```#define MY_ASSERT(...)```
* In my humble opinion, these should contain only ```#defines```
* In my humble opinion, there should be no ```#if``` like statements ever.

## TYPE: app

* *app*: Something that will execute and you can debug. On windows, this is a EXE file. An embedded target it is often an "elf" file.  For Darwin/Linux it a linux binary executable [often this is also an ELF executable]

Example:

```json
{
    "TYPE" : "APP",
    "APP_NAME" : "my-cool-app",
    "SRC_DIRS" : [
        "path/to/src1",
        "path/to/src2"
    ],
    "CMDLINE_INC_DIRS" : [
        "path/to/include"
    ],
    "INCLUDE_JSON" : "path/to/libcommon.json"
}
```

## TYPE: static-lib

* *static-lib*:  A static library, one windows a: ".lib", on Linux and many gnu based tools it is a ".a" file

Example:

```json
{
    "TYPE" : "static-lib",
    "LIB_NAME" : "my-cool-lib",
    "SRC_DIR" : [
        "path/to/partA",
        "path/to/partB"
    ],
    "CMDLINE_INC_DIRS" : [
        "path/to/inc_dir1",
        "path/to/inc_dir2"
    ]
}
```

## TYPE: shared-lib

* shared-lib:  [FUTURE] This generally not supported for embedded targets. On windows this is a DLL, on Linux it is a Shared Object (an .so) file

Note: this is identical to the static-lib, with the exception of the: "TYPE" field.

```json
{
    "TYPE" : "shared-lib",
    "LIB_NAME" : "my-shared-lib",
    "SRC_DIR" : [
        "path/to/partA",
        "path/to/partB"
    ],
    "CMDLINE_INC_DIRS" : [
        "path/to/inc_dir1",
        "path/to/inc_dir2"
    ]
}
```

## TYPE: multiples

* *multiple*: A top level wrapper that builds multiple applications or libraries. Perhaps the best example of this is a series of standalone test case apps. Each one built and compiled as separate projects.

Example: The below creates a total of 8 projects.

3 Application projects, app1, app2 and app3.
Times
3 Board variants, boardA, boardB, boardC

Note that this example uses the APP_NAME as the 
permutation variable.

That would be 9, but there is a DISALLOW for 
that would match the one combination
In this case: "test_app2_boardB"

See below about DISALLOW entries

```json
{
    "TYPE" : "MULTIPLE",
    "APP_LIST" : {
        "path/to/some/app1_project.json",
        "path/to/some/app2_project.json",
        "path/to/some/app3_project.json",
    },

    "PERMUTE" : {
        "PERMUTE_KEY" : {
            "NAME" : "APP_NAME",
            "VALUE": "test_${APP_NAME}_${BOARD}",
        },
        "BOARD" : [ "boardA", "boardB", "boardC" ]
    }

    "DISALLOW" : {
        "VARS" : "APP_NAME",
        "blacklist" : [
            "test_app2_boardB"
        ]
    },
    
    "COMMON" : {
        "INCLUDE_JSON" : [
            "path/to/libcommon.json",
            "path/to/${BOARD}.json"
        ]
    }
}
```

* doxygen: [FUTURE] instructions on how to run Doxygen builds

* coverity: [FUTURE] coverity is a static analysis tool. how to run a static analysis tool.

## Other things that are helpful

### PATHS: Relative and Absolute and the variable: PROJ_ROOT_DIR

Where possible: all things generated are relative to the ROOT directory of the project.

The exception to this "work in process json" files.

You must define some directory that is the ROOT of the project.
The goal is all generated things are relative to that directory.
Or - they will use a macro/variable etc that is that equal.

All path names are relative to the specific JSON file
in your top most JPROJECT file you might have:

```json
{
    "INCLUDE_JSON" : "some/path/foo.json"
}
```

Then later within "foo.json

### The hierarchy of project types

Consider the case where you have many test applications.
And one common library. Your embedded target might not have
enough RAM (or FLASH) to compile and link all test code. You
might need to break up the tests into many different test apps.

#### Strings verses list (arrays)

For some things, one can only enter a single string.
And this makes logical sense. There can be only 1 "APP_NAME"

But for others, there can be one or many. For example:

* "SRC_DIRS" : "path/to/the/source"
* "SRC_DIRS" : [ "path/one/src", "path/two/src" ]

If the KEY name is plural, one can put either a
single string, or an list Both are acceptable.

### Filenames and Directory Names

Often within a JPROJECT one will refer to a filename or a directory.

Rules:

1. always use unix / slashes not DOS \\ slashes.
2. Paths are relative to the JSON file.

Example:

```json
{
    "INCLUDE_JSON" : "some/sub/library/foo.json"
}
```

Then later in ```foo.json``` you might pull in other libraries.

## Suggested Work Flow

* you just have one giant self contained project.
* You will create one of more application projects that use a library.
* you will create one or more library projects

In the one giant (the first case) the result of the build might
be a static-lib or an app - your choice. The entire project
is totally defined in the one giant project.

In the "app" case that project might have:

```json

    {
        "TYPE" : "APP",
        "APPNAME" : "my_cool_app_name",
        "SRC-DIRS" : [
                "./src"
        ],
        "CMDLINE_INC_DIRS" : [
                "./include"
        ],

        "INCLUDE_JSON" : [
            "path/to/library-foo.json",
            "path/to/library-bar.json",
            "and-other-paths"
        ]
    }
```
