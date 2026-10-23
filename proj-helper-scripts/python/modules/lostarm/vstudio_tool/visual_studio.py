from abc import ABC, abstractmethod

from lostarm.make_maker.gen_core import GeneratorCore, register_generator

class GenerateVisualStudio(GeneratorCore, ABC):
    NAME="visual-studio"
    def __init__(self):
        GeneratorCore.__init__(self)
        # TODO ITEMS:
        #  1) Loop over j_project and write each project.
        #  2) Loop over j_project and create filters for ach project.
        #  3) Write the solution file
        # NOTE: in a VS project file there is a magic variable called:
        # ${SolutionDir} - we create everything relative to that variable.

    def generate(self, infilename: str, outfilename: str ):
        self.fatal("WRITE ME")