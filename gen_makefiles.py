import sys

for d in sys.path:
    print("Path: %s" % d )


from makemaker.jproject import Jproject

jp = Jproject()
fn = "testapps/testapps.json"
data = jp.load_root_project(fn)

from makemaker.makemaker import MakeMaker

mm = MakeMaker()
mm.add_project( data )

for proj in mm.all_projects():
    mm.write_project_makefile( )

for tmp in sys.path:
    print(tmp)
    


