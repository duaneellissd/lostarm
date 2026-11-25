# Purpose of this directory

If you workin a "closed" environemnt aka high security enviornment
then the following will be helpful.

a CLOSED environment is closed room with no external connections.
there is no internet connections. This is for high security reasons.

But you still need to install things in some standard way.

How you do that is rather simple.

Step 1 - Get the files into that room. Those steps are:

a) Get approval from the security team for that room.

b) Fetch the files and burn them to a CDROM.

c) Some team performs a "security audit" of that CDROM

d) Physically bring the CDROM into the room.

e) Load the files onto the system.

f) Then to install these files you do this:

   if needed activate your VENV
   cd /to/the/directory/with/the/files.
   pip install -r YOUR-REQUIREMENTS.txt

It is PAINFUL when you miss a dependency.  Thus we list and provide
all dependencies here.


