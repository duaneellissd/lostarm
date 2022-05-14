
import os
import sys
import shutil
import re
import platform
import datetime

AddOption('--unit-test', dest='unittest', action='store_true', default=True)
AddOption('--no-unit-test', dest='unittest', action='store_false', default=True)

import settings

unit_test_enabled = GetOption('unittest' )

args=COMMAND_LINE_TARGETS[:]


# What have we been asked to build?
tmp=len(COMMAND_LINE_TARGETS)
if tmp==1:
   TARGET=COMMAND_LINE_TARGETS[0]
elif tmp==0:
   TARGET=settings.default_target
else:
   print("Only supporting 1 command line target")
   Exit(1)

# is it a valid target we support?
if TARGET not in settings.supported_targets:
   print("SORRY: target %s not supported" % TARGET )
   print("Try one of: %s" % ", ".join( supported_targets ) )
   Exit(1)


# what are the tools (compiler) we will be using?
tools = settings.tool_table[ TARGET ]
   
# Ok, where is our source code
# Where does our (COMMON) source code live?
common_srcdirs=['src/adt','src/debug','src/timer','src/wrapper']

# Where are our source directories
srcdirs = common_srcdirs[:]
# Add the port specific source code

if (TARGET == 'linux'):
   srcdirs.append('port/unix')
 
elif TARGET == 'stm32h7':
   srcdirs.append('port/stm32h7')

#for k,v in Environment().items():
#   print("K=%s -> %s" % ( k, v ) )

# This is the list of unit test functions found
unit_test_functions = dict()
# list of all source files found
src_filenames = []
# Used to detect duplicate filenames in different directories.
# Example:  cat/foo.c and dog/foo.c is not allowed.
basic_filenames=dict()

# used to auto-discover unit test functions.
re_unittest = re.compile( r'^UNIT_TEST_(?P<name>[a-zA-Z0-9_]+)[(]' )

def scan_source_file(fn):
   global src_filenames
   global basic_filenames
   global unit_test_functions

   # we only want C files..
   if not fn.endswith('.c'):
      return
   # Add this to the lis of src files we will compile
   src_filenames.append(fn)
   # Scons cannot handle 2 files with the same name
   # in two different directories
   # Example:   dog/food.c and cat/food.c
   # So disallow rather then quitely fail
   bn = os.path.basename(fn)
   if bn in basic_filenames:
      print("DUPLICATE Basefilename (not allowed)")
      print("OLD: %s -> %s" % (bn, basic_filenames[bn]) )
      print("NEW: %s -> %s" % (bn, fn) )
      Exit(1)

   # If unit tests are disabled... 
   if not unit_test_enabled:
      # Then leave nothing to do
      return
   
   # open and read canidate file.
   with open(fn,"rt") as f:
         lines = f.readlines()
   # does it contain a UNIT TEST?
   for thisline in lines:
      m = re_unittest.match(thisline)
      if not m:
         continue
      name = m['name']
      print("Found Unit test: %s" % thisline.strip())
      if name in unit_test_functions:
         print("DUPLICATE TEST: %s", name )
         print("OLD: %s" % unit_test_functions[name] )
         print("NEW: %s" % fn )
         Exit(1)
      # remember the name and file for later.
      unit_test_functions[name] = fn
         
for sd in srcdirs:
   for rootdir,dlist,flist in os.walk( sd, followlinks=False ):
      for f in flist:
         fn = os.path.join( rootdir, f )
         scan_source_file(fn)

         
print("Found: %d Source files" % len(src_filenames))
if unit_test_enabled:
   print("Found: %d unit tests" % len(unit_test_functions) )

# Deal with command line define quoting.
quoteable = dict()
if platform.system() in ( 'Linux', 'Darwin' ):
   quoteable['"'] =  chr(0x53) + chr(0x22),
   quoteable["'"] =  chr(0x53) + chr(0x27),
   quoteable['*'] =  chr(0x53) + '*',
   quoteable['?'] =  chr(0x53) + '?',
   quoteable['('] =  chr(0x53) + '(',
   quoteable[')'] =  chr(0x53) + ')'
else:
   # Assume DOS..
   raise NotImplementedError("need DOS escape sequences")

def cmdlinequote( value ):
   '''
   Wrap the item in quotes if needed.
   '''
   # Have we been asked to quote this?
   # if so, we quote it here.
   if value.startswith('shellquote(') and value.endswith(')'):
      answer = chr(0x5c) + chr(0x22)
      # then escape out as needed
      for ch in value:
         answer = answer + quoteable.get(ch,ch)
      answer = answer + chr(0x5c) + chr(0x22)
   else:
      # No transformation
      answer = value
   return answer

def _create_defines( input ):
   '''
   Given a string of defines, insert -D infront of each
   and quote the value if required/requested
   '''
   answer=""
   for n,v in input.items():
      if v is None:
         answer = answer + " -D%s" % n
      elif isinstance( v, int ):
         answer = answer + " -D%s=%d" % (n,v)
      elif isinstance( v, str ):
         answer = answer + " -D%s=%s" % (n, cmdlinequote(v))
      else:
         print("Unknown CMDLINE define type for %s" % v )
         print("Maybe you need to quote it?")
         Exit(1)
   return answer

   
env = Environment()
tmp=_create_defines( settings.defines_table[TARGET] )
env['CFLAGS'] = tmp + " " + settings.cflags_table[TARGET] 
tmp=settings.include_dir_table[ TARGET ]
print("TMP=%s" % tmp )
env['CPPPATH'] = tmp

for k,v in settings.tool_table[TARGET].items():
   env[k] = v


HERE= Dir('.').srcnode().abspath
BUILD_DIR=os.path.join(HERE, settings.build_dir)
GEN_INC_DIR=os.path.join( BUILD_DIR, TARGET, 'include', 'generated' )

if os.path.isdir(BUILD_DIR):
   print("DELETE gendir: %s" % BUILD_DIR )
   shutil.rmtree( BUILD_DIR )
print("CREATE gendir: %s" % BUILD_DIR )
os.makedirs( BUILD_DIR )
os.makedirs( GEN_INC_DIR )

def _c_quote( s ):
   result = ''
   for ch in s:
      if ch in (chr(0x22),chr(0x5c)):
         result += chr(0x5c) + ch
      else:
         result += ch
   return chr(0x22)+result+chr(0x22)


print("Enabled: %s" % unit_test_enabled)
if unit_test_enabled:
   env['CPPPATH'].append( GEN_INC_DIR )
   fn=os.path.join( GEN_INC_DIR, "generated_unittest.h" )
   print("Creating: %s" % fn )
   with open(fn,'wt') as f:
         f.write("#include <lostarm/lostarm.h>\n")
         f.write("#ifndef LOSTARM_GEN_UNIT_TEST_H\n")
         f.write("#define LOSTARM_GEN_UNIT_TEST_H \"b7b79e22-9dd8-458d-8ae8-21759a6b744a\"\n")
         f.write("// Generated: %s\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
         for func,filename in unit_test_functions.items():
            f.write('DECLARE_UNIT_TEST( %s, %s, %s )\n' % (func,_c_quote(func), _c_quote(filename)))
         f.write('\n\n')
         f.write("UNIT_TEST_TABLE_DECL(%d)\n" % len(unit_test_functions))
         f.write('#if UNIT_TEST_TABLE_C\n')
         f.write("UNIT_TEST_TABLE_START(%d)\n" % len(unit_test_functions))
         for func,filename in unit_test_functions.items():
            f.write("  UNIT_TEST_TABLE_ENTRY( %s, %s, %s )\n" % (func, _c_quote(func), _c_quote(filename)))
         f.write("UNIT_TEST_TABLE_END()\n\n")
         f.write("#endif /* UNIT_TEST_TABLE_C */\n")
         f.write("#endif /* LOSTARM_GEN_UNIT_TEST_H */\n")
            
                 
env.StaticLibrary('liblostarm', src_filenames )



# Local Variables:
# mode: python
# End:
