'''
The purpose of this: "gen_proj_file.py" is to:
   A) Read the base project json file, which results in a dict.
   B) Expand that dict with 'features'
   C) Save that expanded dict.

The Purpose of the "gen_makefile.py"
    A) It reads the above expanded dict.
    B) It produces a Makefile that builds the application makefile.

The purpose of the "gen_xcode.py"
    a) Like above it reads the expanded dict.
    b) It produces an MAC xcode project file

The purpose of the "gen_vstudio.py"
    a) Like above it reads the expanded dict.
    b) It produces a visual studio community edition project file

The purpose of the "gen_stm32cube.py
    a) Like above it reads the expanded dict.
    b) It produces a STM CubeSuite (Eclipse) Project file

The purpose of the 

'''
import sys
import os
from lostarm.gen_project import ExpandJsonProject


class MyMain(ExpandJsonProject):
    def hook_modify_project(self) -> None:
        # This hook exists so we can "modify" the json/dict.
        # In this example it do nothing.
        pass


def main( args : list[str] ):
    tool = MyMain()
    tool.main( args )
    sys.exit(0)

def case0():
    main( sys.argv )

def case1():
    args = []
    args.append( sys.argv[0] )
    # We need to define where the PROJ_ROOT_DIR is located.
    here = os.path.dirname(os.path.abspath(__file__))
    args.extend( ["-D", 'PROJ_ROOT_DIR=${CWD}'] )
    # Where are we putting output files? Define that variable.
    args.extend( ["-D", 'OUT_DIR', os.path.join( here, 'out-dir') ])
    # What is the root JSON Project file?
    args.extend( ["--root-proj", "testapps/hostonly_helloworld/hostonly_helloworld.json"] )
    # We read that jproject file and expand it to this.
    args.extend( ["--output", "${OUT_DIR}/host_only_helloworld.jproject"] )
    main( args )

if __name__ == "__main__":
    # case0()
    case1()



