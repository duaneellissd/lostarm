# Shell Variables.

This is about shell variables.

There are more Markdown files in the DOCS dir.

      [Click here For More Markdown Files](docs)

## The variable:  ```PROJ_ROOT_DIR```

   This must point at the root of your project.
   This is where the 'root' .git directory is located.

   If you have two copies of the package checked out They must be in
   two different directories.

   There must exist a file ${PROJ_ROOT_DIR}/project_settings.sh one
   must "source" this file to use the project.

## TO SWITCH projects.

   Exit the shell, (or log out log back in) and then "source" the
   other one in the other directory.

## Variable NAME convention, _DIR variables

   RULE: Always points to a Directory.

   If it ends with DIR in any form Then the value points to a
   directory of some sort.  Often a FULL absolute path.

   Of note: In various Microsoft tools, (Visual Studio) has
   variables within the Project files, ie: ```${SolutionDir}```

   In those microsoft tools the rule is different.  If the name ends
   with "dir" then the variable value also ends with a backslash.

   We do not do that. We expect YOU to insert the slash.
   
## Variable NAME convention, _EXE variables

   RULE: Always point to an executable.

   YES, we know Linux does not put "EXE" on the end of files, and EXE
   is really a windows thing.

   That said it is a Naming convention. Much like the hungarian form
   popularized by Microsoft, ie a variable name starting with "p" indictes
   the variable is a pointer.

   Same thing here, just like variables ending with _DIR

## Linux _EXE vrs _ELF variables:

   Yes we understand that EXE is a windows thing.  But Linux has
   executables too. On Linux an EXE can be an ELF, or a "chmod +x"
   shell script it does not matter, as far as we are concerned it is
   an EXE.

   An _EXE is always an executable for the HOST system.
   
   AN _ELF is always an executable for the CROSS TARGET system.

