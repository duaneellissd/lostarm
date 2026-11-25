# Whats going on with the Python Packages.

## First - the local modules under ${PROJ_PYTHON_DIR}/modules

   These are not intended to be part of PyPy.
   Reason: Often in an embedded (bare metal) world one does
   additional steps and having the ability to have the modules
   locally make it simple to hack, modify or update them.

## Second - While we try to avoid gratuitous use of Python modules
   There are a few we do make use of.

   And we prefer a WHL (wheel) file because they are universal.

## We do not pull these from PyPy, we have our own private copy.
   WHY? Because I work in what is called a "closed environment".
   I have no internet where I work for my $job$ this is for security reasons.
   And so PIP can work two ways:

### Method 1 - pull from some external PyPy like place.

### Method 2 - install the whl file directly.

    So we choose Method 2.

    So if we list the Packages in dependency order in the requirements file
    then PIP does not need to go search on line for the dependencies.

    