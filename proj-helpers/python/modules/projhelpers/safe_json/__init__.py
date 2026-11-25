"""
ALl debug output and fatal things go through the _DebugOutput class.
Note:
    1) This is class is effectively a singleton.
    2) Below we have a global: "debug_output"
    3) Other things use VerbosePrint() which uses the single common _DebugOutput class.
"""
from projhelpers.safe_json.safe_json import safe_json_load, safe_json_save
