import os
import sys

sys.path.insert(0,'../../modules')

from builder import TopLevel

my_toplevel = TopLevel()
my_toplevel.read_settings('../../toplevel.settings.json')

app = my_toplevel.new_app('testcase')

app.require_lib('debug')
app.require_lib('board')

app.build('Debug')

