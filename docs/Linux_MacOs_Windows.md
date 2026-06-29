# Linux, MacOs, Windows Issues.

## SLASH TYPES:

   When dealing with Windows things, in our scripts we follow the
   general rule that Microsoft seems to prefer backslashes but seems
   to accept unix slashes.

   So where ever you see things, please do not go changing slashes.

   Flipping slashes around is a painful thing to fix and get correct.
   Thus within code, and scripts we exclusively use Unix slashes.

   When generating things that are for Windows only we tend to
   generate things with Windows Backslashes. But that is not a
   garentee.

## Linux verses Darwin (aka: MacOS)

   We'll often use the phrase Linux, we generaly mean both.  The
   orginal authors laptop is an INTEL MAC, that may change But today
   it is an Intel MAC... So that author has a vested interest in
   making things work on a MAC.

   That said, the author also has a number of Linux machines at
   home and so things also run on Linux.

## Windows Subsystem For Linux (WSL) - Sorry.

   While we are not actively hostile to this, but we are already
   supporting 3 systems, (MAC, LINUX and Windows)... a forth makes it
   hard to get things done.

   That said, after doing things 3 ways - often the 4th is simple.  If
   there are specific problems please point them out offer a patch.
   The author simply does not have the time to test/develop on a 4th
   platform.

   Another annoying thing: Why can't I invoke a windows command from
   WSL, and why can't I invoke a linux command from Bat files.
   Agh... Please stop this nonsense.

## Not everyone uses Linux, Please I need WindBlows.

   Yea, we recognize not everyone uses Linux or a Mac Some of you are
   on "WindBlows". We do try to go out of our way to support this
   whever ever possible.

## Windows Scripting - Batch or Powershell.

   In most cases, we prefer a batch file.

   Yes we are aware that Powershell is a thing these days.

   PS scripts seem to be loved by Windows ADMINS however many Linux
   users see Power Shell as a "three headed alien from mars"

   So to that end - we mostly write "BAT" files.
   Where we generate things we try to generate a "PS1" script too.

## Wrapper scripts - The language of choice is Python.

   Sometimes it is just too complex to write Something in bash.  Then
   write it again in PowerShell or something else.

   So instead, we write a small simple "shell/batch/ps1" script that
   simpliy invokes a larger more complete Python script.

