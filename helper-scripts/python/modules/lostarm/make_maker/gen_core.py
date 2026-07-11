import os
from abc import ABC, abstractmethod
from lostarm.jproject import Jproject
from lostarm.utils import VerbosePrint
from lostarm.variables import get_global_vars

__ALL__ = ["GeneratorCore", "register_generator", "get_generator" ]

_all_generators = dict()

def register_generator( klass : "GeneratorCore" ):
    global _all_generators
    tmp = klass()
    if tmp.NAME not in _all_generators:
        _all_generators[tmp.NAME] = klass
        return
    tmp = VerbosePrint()
    tmp.fatal("%s already registered" % name)

def get_generator(name: str) -> "GeneratorCore":
    cls = _all_generators.get(name)
    if cls is None:
        tmp = VerbosePrint()
        tmp.verbose_print(0, "Generator: %s not registered" % name)
        tmp.verbose_print(0, "Known generators are:")

        for this_name in _all_generators.keys():
            tmp.verbose_print(0, "    %s" % this_name)
        tmp.fatal("Sorry cannot continue")
    tmp = cls()
    return tmp


class GeneratorCore(VerbosePrint,ABC):
    def __init__(self):
        VerbosePrint.__init__(self)
        ABC.__init__(self)
        self.variables = get_global_vars()

    def find_template(self, sub_dir_name : str, name : str ) -> str:
        """
        Often a generator uses a "fragment file" or a "template"
        Makefiles are an example of that.
        example:
            a Makefile.in might have @INCLUDE( "basics.mak" )@

        How it works:
        1) Each generator has a name.
        2) This becomes: ${HERE}/templates/${NAME}/basics.mak
        3) Where ${HERE} is the directory where this file lives.
        4) And ${NAME} is the name of the generator.
        """
        here = os.path.dirname(os.path.abspath( __file__ ))
        fn = os.path.join(here, self.name, sub_dir_name, name)
        return fn


    def resolve_text(self, s: str) -> str:
        """
        Given a string with ${VARS} resolve the ${VARS}
        """
        return self.variables.resolve(s)

    @abstractmethod
    def generate(self, project : Jproject, infilename : str, outfilename: str ) -> None:
        self.fatal("A generate function was not provided by the derived class")
