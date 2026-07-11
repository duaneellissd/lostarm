from abc import ABC

from lostarm.utils import VerbosePrint
from lostarm.make_maker.gen_core import GeneratorCore, register_generator,get_generator

class GenerateMakefile(GeneratorCore, ABC):
    NAME = 'makefile'
    def __init__(self):
        GeneratorCore.__init__(self)
        # In our generated makefiles, we write all file references
        # Relative to the ${PROJ_ROOT_DIR}
        # THUS - provided the user has set the "PROJ_ROOT_DIR"
        # the makefile can be placed anywhere.

    def generate(self, infilname : str, outfilename : str ) -> None:
        self.fatal("WRITE ME")

