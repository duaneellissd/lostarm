from abc import abstractmethod, ABC
import argparse
import os
import sys
from lostarm.utils import VerbosePrint, safe_json_load, safe_json_save
from lostarm.jproject import Jproject
from lostarm.variables import get_global_vars, Variables
from lostarm.make_maker import GeneratorCore, get_generator
from lostarm.vstudio_tool import GenerateVisualStudio

class GenProjectMain(VerbosePrint, ABC):
    def __init__(self):
        VerbosePrint.__init__(self)
        ABC.__init__(self)
        self.j_project : (Jproject|None) = None
        self.args : argparse.Namespace = argparse.Namespace()
        self.generator : (GeneratorCore|None) = None
        self._shell_vars : Variables = get_global_vars()
        self._shell_vars.add_default_vars()

    def parse_cmdline_args( self, arg_list : list[str] ) -> None:
        """
        Parse command line parameters for this tool
        """
        ap = argparse.ArgumentParser( description="a project creation tool",
                                      prog=arg_list.pop(0))
        ap.add_argument( "-v", dest='VERBOSE', default=0, action='count',
                         help="Increase verbosity" )
        ap.add_argument( "--output", dest='OUT_TYPE',
                         default=[], action='append', nargs='+',
                         help="Specify the output type")
        ap.add_argument( "-D", dest="VARS", help="Define variable in form NAME=VALUE",
                         action='append')
        ap.add_argument( "--root-proj", dest="ROOT_JSON", required=True,
                         help="Specify root json project file")
        ap.add_argument( "--out-dir", dest="OUT_DIR", required=True,
                         help="Specify where generated project files go")
        ap.add_argument( "--infile", dest="INFILE", default=None,
                         help="input template filename")
        ap.add_argument( "--outfile", dest="OUTFILE", default=None,
                         help="output file to be generated")
        self.args = ap.parse_args(arg_list)
        if len( self.args.OUT_TYPE ) == 0:
            self.fatal("No Output project types where specified")

        self.args.ROOT_JSON = os.path.abspath( self.args.ROOT_JSON )
        self._shell_vars.add_variable('ROOT_JSON', self.args.ROOT_JSON )
        self.args.OUT_DIR = os.path.abspath( self.args.OUT_DIR )
        self._shell_vars.add_variable( "OUT_DIR", self.args.OUT_DIR )
        self.set_verbosity( self.args.VERBOSE )
        # parse variables
        for var in self.args.VARS:
            if '=' not in var:
                print("%s\n" % ap.format_usage() )
                self.fatal("Expected -D NAME=VALUE, got: -D %s" % var )
            else:
                n,v = var.split("=",1)
                self._shell_vars.add_variable( n,v )
        self.fatal_where_push("command-line", 1 )
        self._shell_vars.resolve_all_vars()
        self.fatal_where_pop()

    def load_root_project(self) -> None:
        """
        Loads and expands the root project.
        """
        self.j_project.load_root_project(self.args.ROOT_JSON)

    def resolve_text(self, s : str ) -> str:
        """
        Given some text with ${VARS} convert the vars to strings.
        """
        # NOTE: So
        return self._shell_vars.resolve_text(s)

    def dump_filename(self) -> str:
        out_dir_name = self.resolve_text("${OUT_DIR}")
        if not os.path.isdir(out_dir_name):
            os.makedirs( out_dir_name )
        fn = os.path.join(out_dir_name, "all-projects.dump.json")
        return fn

    def save_dump_file(self) -> None:
        self.j_project.save_to_file( self.dump_filename() )

    def load_dump_file(self) -> None:
        self.j_project.load_from_file( self.dump_filename() )

    def create_output_files(self) -> None:
        assert len(self.args.OUT_TYPE ) > 0
        for type_name in self.args.OUT_TYPE:
            self.generator = get_generator(type_name)
            ifilename = self.args.INFILE
            ofilename = self.args.OUTFILE
            self.generator.generate( self.j_project, ifilename, ofilename )


    @abstractmethod
    def hook_modify_project(self) -> None:
        """
        This hook is so that you can add features as needed
        after the project has been loaded.
        """
        # for now, this does nothing.
        return
    def main(self, cmdline_args : list[str] ) -> None:
        self.parse_cmdline_args(cmdline_args)
        self.j_project = Jproject()
        self.load_root_project()
        self.save_dump_file()
        # release the parsed and expanded data.
        self.j_project = None
        # Reset the JProject.
        self.j_project = Jproject()

        self.create_output_files()
        # Done.
        sys.exit(0)
