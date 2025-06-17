# How the TEST Files work

This directory contains test files for the JsonReader() class.
Files are named as follows:

## File type "in_*.json"

in_NAME.json  <- Is an input file

One of two matching files must exist:
Option 1)  out_NAME.json
Option 2)  out_NAME.error

## File type: "out_*.json"

out_NAME.json <- Is the expected result if it parses correctly.

## File type: "out_*.error"

out_NAME.error <- If the parsing results in an error.

Note: There are many types of errors and we do not test these exactly.
Instead - the error checking is simple and basic.
The error file contains a single word and that word should occur in the "fatal" message.
If not the error test fails
