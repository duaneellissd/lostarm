# lostarm

## Getting started

## Step 1: Assuming you have done the GIT CLONE

   This directory is known as ${PROJ_ROOT_DIR}
   This directory is where this README.md file is located

## Step 2: You need to type a few more commands:

   cd ${PROJ_ROOT_DIR}
   git submodule init
   git submodule update  <-- This populates the "proj-helper" director.

## STEP 3: If you have not done so, you will need to set a variable:

   export PROJ_PYTHON_EXE=/path/to/your/python/executable

   I suggest you add this to your ${HOME}/.bashrc file.

   Details are here: [```${PROJ_ROOT_DIR}/proj-helpers/docs/ALL_ABOUT_PYTHON.md```](proj-helpers/docs/ALL_ABOUT_PYTHON.md)

## There are a lot more Markdown docs located here

   [`${PROJ_ROOT_DIR}/proj-helpers/docs`](docs)

## Future there will be more here.

   [`${PROJ_ROOT_DIR}/docs`](docs)

## Step 4: Linux/Mac only (for now, FUTURE: Windows...)

   bash$ cd ${PROJ_ROOT_DIR}   <-- Where you checked this out.
   bash$ . ./source_me.sh      <-- Source this file.

The above "./source_me.sh" script will do the following:

   a) Setup a number of ENV Variables.
      Details [```${PROJ_ROOT_DIR}/proj-helpers/docs/ENV_VARS.md```](proj-helpers/docs/ENV_VARS.md)

   b) If ${PROJ_ROOT_DIR}/.venv does not exist it will be created.
      This is a standard Python Virtual Enviroment.

      If you want to recreate it, delete the directory
      and re-run the 'source_me.sh' script.

   c) I use a combination of PyCharm, VSCODE and Emacs as my IDE.

   d) So - it also creates a ${PROJ_ROOT_DIR}/.vscode directory.
      and it will populate it with helpful features.
      and it will create ```${PROJ_ROOT_DIR}/start_code.sh```
      NOTE: If start_code.sh exists the process skips it.
            If you want it updated, delete it and run sourceme again.

   e) And for PYCHARM users, it will create:
          ```${PROJ_ROOT_DIR}/start_pycharm.sh```
      If start_pycharm.sh exists the process skips it.
          If you want it updated, delete it and run sourceme again.

## Step 5: Building a Hello World app (Linux Host)

1) `cd ${PROJ_ROOT_DIR}`
2) `cd hello-world`
3) `bash ./build.sh --target=host`

## Step 6: An FYI - I use the 'ci_build.sh' to test things.

   If you want to contribute
   Rule #1 - Thank you.
   Rule #2 - You must run ci_build.sh and it must work without error
   Rule #3 - and it must not have any compiler warnings.
   Rule #4 - All self/unit tests must pass, see ci_unittest.sh

## Going further ... other targets: (Future, not ready yet)

   cd ${SOME_DIRECTORY}

   bash ./build.sh --target=NAME.
