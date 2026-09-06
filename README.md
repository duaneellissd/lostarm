# lostarm

## Getting started.

## Step 1: Assuming you have done the GIT CLONE

   In this Markdown file, this is known as the ${GIT_CHECKOUT_DIR}

   This directory is also known as the ${PROJ_ROOT_DIR}

## There are alot more Markdown docs located here:

   ``${PROJ_ROO_DIR}/docs```

# Step 2: Linux/Mac only (for now, future: Windows using GIT BASH)

# Step 3: This tool makes extensive use of Python.

  And you must set an ENVIRONMENT variable as follows
  (Typically you would do this in your .bashrc file)
  
      export LOSTARM_PYTHON_EXE=/path/to/your/version/of/python

  Once added to your ${HOME}/.bashrc, logout and log back in.

  And yea, a python VENV is not going to work too bad.
  Please read: ${PROJ_ROOT_DIR}/ALL_ABOUT_PYTHON.md for details.
  
```cd ${PROJ_ROO_DIR}```

OPTION 1:

Step 3: bash ./ci_build.sh	-> should build everything.

OPTION 2:
       bash ./build --cross path/to/cross-file --build path/to/projectdir

       Where the cross-file defines the tools you are using.
       By default, the "path/to/cross-file" is for your host OS (linux/mac)
       
       And the project dir is the root of the [test app] you want to build.

About a few directories:
      ```${PROJ_ROO_DIR}/cross```
	This directory holds
      



Step 3: source ./all_settings.sh


Step 4: bash ./smoke_test.sh (this runs a selftest host only)


## History 
An ARM CortexM3 environment

This started years ago on SourceForge, this is an major update to that package

I have seen questions on Reddit.com/r/embedded about how to do something, I've needed a working baseline.

This is that baseline from which I create examples.


