# WTF are these?

These are attempts to fix thing in common compiler header files.

For example GNU systems provide a function: strcasecmp()
This is normally found in #include <strings.h>

BUT - Visual Studio does not, nor does KIEL, nor does ... etc
   This where/why things like: "cmake" and "gnu-autoconf" step in.
   They generate a giant: "config.h" file or simular
   And this devolves into a lot of #if/#else/#endif crap in your code.
   I want to avoid that and make it go away.

TO fix that problem, you have 2 options:

Option 1 - YUCK!
   Put #if/#else/#endif all of your code.
   
Option 2 - Provide a FIX in a common header file.
   This limits the problem to just a few header files.
   IT is better to fix this in ONE PLACE in ONE Header file
   and not need to fix it in every damn C file on the planet.

Thus, in your code you do this instead:
      #include <lostarm/wrapped/_string.h>

      In many cases, the wrapped file is effectively empty.
      BUT - when needed, it is helpful and a simple solution.

# Secondary rules:
    There is a sub-source-code-module, called: lostarm/src/missing
    When/where we must adapt or provide a missing function.
    This is where we place that source file.

    The options we have are:
    	Option 1 - create a macro:  #define strcasecmp(A,B) _stricmp(A,B)
	Option 2 - create a macro:  #define strcasecmp(A,B) MISSING_strcasecmp(A,B)

    If needed, the "MISSING_" function should be found in lostarm/src/missing.

# Additional example:
    We try where possible to use the GNU/GCC standard names.
    For example in <lostarm/endian.h> we discover the endian things.
    GCC has certian names - great we leave these alone.
    Visual Studio uses other names, GRR.
    So - when we discover Visual Studio we add the matching GCC macros.
    This also applies to builtin functions.
