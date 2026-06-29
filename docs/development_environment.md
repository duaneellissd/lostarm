## MINGW - vrs Visual Studio? Verses Linx xo

   Again, it is painful to setup yet another thing.  But this is
   something the original author wants to avoid but may be backed into
   a corner and forced to make happen. GRRR!!!


## The general goal here is the user needs to install only this.

   1) Python - preferably Python 3.11 or later.
   2) They need to set the variable: "PROJ_PYTHON_EXE" accordingly.
   3) On a MAC - install XCODE - it comes with clang/gcc.
   4) Linux - install GCC for the host and the normal build tools.
   5) On windows, install Visual Studio (not talking about VS CODE)

   6) At that point, everything should just work.

## What about Ruby, or Tcl, Rust, Haskel, or Whatever.

   NO - the "complex host language of choice here is Python".

   Python is ubiquous and avaialbe on all of our targeted platforms.

   One can easily write a small 5 to 10 line wrapper that invokes Python.

   All of the heavy lifting can easily be done in Python.

   We have no plans to support or accept submissions and/or
   contributions that make use of some other language, or need some
   other package.

   Python is very powerful. It is very full featured.  and you can
   write just about anything you need using the python standard
   library.

   There is another philisophical reason for this.

   Also think of your victims. The others who want to use this system.
   The others who will edit, hack use and maintain this system beyond
   you. To support "+1 more" lanaguage that means all developers
   become victims of your decision. All contributors need to install
   that "+1 more language" - UGH we want to avoid that.

   They probably already have Python installed, or it is easy for them
   to do that. Having them install yet another "+1 more language" is a
   source of problems we want to avoid.

   And - maybe the version of that "+1 more language" is not so easy
   to setup on all supported systems. (Linux, Darwin and Windows).

   Do you have all 3 systems? Can you debug on all 3 systems?  Does
   the next contributor have that system too? And is it configured
   in a way that they can be successful?

   That answer is generally NO, so that is another reason Python only.

## Docker, Container, whatever.

   NOPE - again not going there.

   DOCKER and containers have a place. This is not one of them.

   A) If you are providing a "micro service" - then putting your
   microservice in a container makes sense.  It is a "chroot jail"

   If it gets cracked, or you need more, they are easy to spin up.
   and easy to shut down when they are no longer needed.

   B) In many orgs, the IT team is a windows only team. And they look
   at Linux as if you are a 3 headed alien. They cannot support you.

   Thus the engineering team does Linux on their own.

   Every engineer sets up linux another and different way.  You end up
   with situations where: "it builds for ALICE on the ALICE machine"
   but it does not work for BOB on the BOB machine. This is chaos.

   The engineering manager goes to the IT team and asks for help.
   The IT leader gives up - because they do not have the skill set.

   So engineering "engineers" around the IT TEAM by using Docker.
   When the proper answer would have been: "Hire a proper DEV OPS Team
   (or person)"

   Containers are a result of an IT TEAM who cannot do their job.

   Why don't you solve the first problem first.  Then you will not
   have the second problem.

## Another example:

  Have you ever "edited source code" on computer (A), then copied your
  source code to computer (B) to compile, then copy the result to
  computer (C) to debug the source code?

  The IDE does not like that. And you make a tweak on machine (B) or
  (C) to debug a problem and it never gets propigated back to machine
  (A). My experience with containers is exactly like that.

## more specific case:

   1. Compiler compiles the source code.
   2. OBJ contains /some/path/to/some/filename.c
   3. That path is correct for which of the 3 machines (A) (B) or (C)?
   4. Source level debugger (GDB or IDE) says WHERE is that file?

   Having everything work on your desktop is easyier to make work.

* BESIDES:

   The EDIT, COMPILE, DEBUG, TEST loop is already hard enough to
   setup.  Doing that inside a container is hard enough.

