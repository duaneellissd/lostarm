# Purpose of the _wrapped directory.

# Number 1 goal is to remove/replace/fix #if/#else/#endif in application code.

Often a C file needs to include some standard system header file, for example string.h
however the target implimentation is missing something

Or that target needs various #defines turned on prior to including the file

The goal here is to provide a baseline wrapper for the standard headers
that turn on various basic features that are GNU like.

for example,  strcasecmp() does not exist in Visual Studio
instead it is called _strnicmp() - thus the string.h file a solution.

Option 1:
   #define strcasecmp()  to some MISSING_strcasecmp() replacement.

   You'll need to create/provide an implimentation of MISSING_strcasecmp()
   Or what ever function you need in the missing directory/library.

Option 2:
   #define strcasecmp() to _strnicmp() for visual studio wraped with #ifdefs

The general view is this:

   #ifdefs in header files are not horrible they are done once and only once.
   #ifdefs in CODE files are repeated through out the project.

   By solving the issue once in the header we reduce the number of #ifdefs

# RULE / USAGE

Step 1

    Application code #include <lostarm/wrapped/_STDNAME.h>
    
Step 2

     The file wrapped/_STDNAME.h
     Turns on what ever #defines are required
     And/or creates additional function prototypes (ie: missings)

     Then, the wrapped header includes the <stdname.h> file.
     

   
  