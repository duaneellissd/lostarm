
import os

from jproject import Jproject

jp = Jproject()

jp.load_root_project( "hello_world.json" )
jp.set_variable("PROJ_ROOT_DIR", os.getcwd() )

ijp_fn ="intermediate.jproject"
jp.save_project_as_json( ijp_fn )

jp = None


from makemaker import MakeMaker

mm = MakeMaker()

mm.load_jproject( ijp_fn )
mm.set_type("host-gcc")
mm.generate_makefile( "Makefile.gcc" )

mm = None

mm = MakeMaker()
mm.load_jproject( ijp_fn )
mm.set_type( "host-clang" )
mm.set_type("Makefile.clang" )

mm = None

from bashbuilder import BashBuilder
bb = BashBuilder();
bb.set_gcc_compiler_CROSS_COMPILE_PREFIX("")
bb.generate_bash_script("bash_build.sh")


