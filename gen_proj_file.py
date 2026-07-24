import sys
from lostarm.make_maker import register_generator
from lostarm.gen_project import GenProjectMain
from lostarm.make_maker.gen_core import register_generator
# We want to support Makefiles so we import this.
from lostarm.make_maker import GenerateMakefile
from lostarm.vstudio_tool import GenerateVisualStudio


register_generator( GenerateVisualStudio )
register_generator( GenerateMakefile )


class MyMain(GenProjectMain):
    def hook_modify_project(self) -> None:
        # We do nothing here.
        # we could but this example does not.
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
    args.append('-v')
    #args.extend( ["-D", 'FOO=BAR' ] )
    #args.extend( ["-D", 'FOO2=BAR2' ] )
    args.extend( ["-D", 'PROJ_ROOT_DIR=${CWD}'] )
    args.extend( ["--root-proj", "testapps/hostonly_helloworld/hostonly_helloworld.json"] )
    args.extend( ["--out-dir", "./outdir" ])
    args.extend( ["--output", "Makefile" ])
    main( args )

if __name__ == "__main__":
    # case0()
    case1()



