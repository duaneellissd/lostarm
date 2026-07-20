# The Template PreProcessor

This was inspired by: the GNU @NAME@ replacement features
used by the GNU AutoConf tools - which are great if your
only world is Linux and never windows. 

Please do not suggest CYGWIN, I've known about it for over
25 years, and still do not like it. So I created this tool.

## Dealing with parse errors.

This parser gives up quickly. Better parsers try to recover
and give you more error messages. GCC is an example of a good
parser, GCC tries to keep going after an error. This does not.

You'll notice that this preprocessor is not very pythonic. This
is a purposeful choice. Python libraries tend to throw exceptions. 

Instead, it generally calls the fatal() function and exists.

WHY? Because this is a tool, human users of a tool probably
do not want to see or debug what I call: "python vomit"
(the stack backtrace when a pyhon exception occurs).

If this tool produces Python VOMIT it is a bug in the tool.

Instead, good human tools should output a standard IDE 
clickable error message. A good example of this is GCC, 
when it issues an error message you see the following:

* Syntactically:  FILENAME:LINENUMBER: ERROR Message
* Example:  foo.c:1234: ERROR undefined variable: bar.

## The PreProcessor vrs the Template engine vrs a Tool.

All use the same syntax, they are layered on top of each other.

* PreProcessor handles only basic "c-pre-processor" like things.
* The Template Handles more things
* At top of the food chain is a TOOL
* Example: MakeFileGenerator or ProjectGenerator
* The TOOL adds domain specific @NAMES@ 

Thus, if you want to understand how @NAME@ works..
You may need to look in different places.

## Things we support:

### @MACRO_BEGIN(name)@ and @MACRO_END(name)@

The @MACRO@ feature exists to help the Makefile template.
And it is best understood using the context of Makefile
creation or generation.

RULES:
    Each Macro must have a unique name.  Macros 
    effectively "record" the text between BEGIN and END.

When Invoked, the @MACRO@ is effectively acts sort of like
a mini-include file

Example: 

* When processing the list of source files
* We play back a macro for each source file.

### @INCLUDE( filename )@

Filenames can be quoted, or unquoted. Quotes must match.
Filenames may contain ${VARIABLES}

Note you must supply the search directory entries.

By default, the first place searched is relative to 
the current input file.

### @INCLUDE_ADD_SEARCH_DIR( dirname )@

Dirnames may contain ${VARIABLES}
Dirnames may be quoted or unquoted, quotes must match.

This is an alternate to the application calling add_search_dir()
This lets a data file add additional search directories.

### @IF(expression)@, @ELSE@, and @ENDIF@

There are limitations:

The expression is "neutered" before being evaluated.
These expressions must be on a line by themselves.
you cannot do this:

```
    @IF_DEFINED(fooBar)@
    ...
    @ENDIF@ # foobar <-- Comment is not supported.
```

## @ELSE_IF(expression)@ and friends.

These are also supported:

   * @IF_DEFINED(name)@
   * @IF_NOT_DEFINED(name)@
   * @ELSE_IF(expression)@
   * @ELSE_IF_DEFINED(name)@
   * @ELSE_IF_NOT_DEFINED(name)@

## SECURITY Expression consideration:

To simplify expression parsing we use pythons eval()
function, which tends to set of red-flags from
various security people.  Don't fret, we effectively
neuter (cut the balls off) any expression so that it 
cannot do much.

The neutering rules we use are:

* The neutering process is a heuristic maybe you can improve it.
* There must be a balanced number of ()s.
* All Python binary operators are supported including bitwise.
* Python keywords AND/OR/not, must have ()s before and after.
* Example:  Illegal:  not True,   Legal:  not (True)
* Example:  Illegal:  4 and 5, legal: (4) and (5) is required.
* The function defined() becomes 1 or 0 if a variable is defined.
* Defined means: (A) it is the shell_like_varable
* defined(NAME) tests if the variable or os environ exists.
* The defined(NAME) is a case-sensitive test.
* Names like @FOO@ are replaced with variable values.

## Day in the life:

```python
    
from lostarm.preprocessor import PreProcessor
pp = PreProcessor()
pp.add_search_dir("/path/to/some/place")
pp.open("some_file.txt")
at_eof = False
s = "" # Make PyLance be quite, initialize this.
while not at_eof:
    try:
        s = pp.next_preprocessed_line()
        # remove trailing white space newline.
        s : str = s.rstrip()
    except EOFError:
        at_eof = True
    # these track "@INCLUDE(filenames)@
    fn = pp.cur_filename()
    ln = pp.cur_lineno()
    print("%s:%d is: %s" % (fn,ln, s ))

 ```  


