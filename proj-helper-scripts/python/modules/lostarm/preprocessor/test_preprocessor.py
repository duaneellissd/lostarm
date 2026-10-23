import os
import unittest
from lostarm.preprocessor import PreProcessor
from lostarm.utils.verbose_print import set_unit_test_mode, UnitTestException

class TemplateTester( PreProcessor ):
    def __init__(self):
        PreProcessor.__init__(self)
        set_unit_test_mode()
        self.actual = []
        self.expect_fail = False

    def parent_hook(self, text) -> tuple[bool,str]:
        if self.expect_fail:
            self.actual.append("EXPECT ERROR: %s" % text )
        return super().parent_hook(text)

def get_filename( prefix : str, fn :str ):
    tmp = os.path.abspath(__file__)
    tmp = os.path.dirname(tmp)
    tmp = os.path.join( tmp,'test-preprocessor', prefix, fn )
    return tmp

TT = None

class TestPreProcessor(unittest.TestCase):
    def simple_test(self, fn : str ):
        # This tests includes
        ifn = get_filename( "test-in", fn )
        efn = get_filename( "test-expected", fn )
        afn = get_filename( "test-actual", fn )
        global TT
        TT = TemplateTester()
        TT.open(ifn)
        TT.actual = []
        done = False

        this_line = ""
        TT.expect_fail = False
        while not done:
            last_line = this_line
            try:
                this_line = TT.next_preprocessed_line()
                self.assertFalse( TT.expect_fail )
            except EOFError as eof:
                done =True
                continue
            except UnitTestException as e:
                self.assertTrue( TT.expect_fail )
                this_line = "had-error-as-expected\n"
            TT.expect_fail = ('_NEXT_LINE_FAILS_' in this_line)
            if '_INVOKE_MACRO_' in this_line:
                this_line = this_line.strip()
                this_line = this_line.replace('_INVOKE_MACRO_','').strip()
                # what remains on the line is the macro we should invoke.
                if this_line.startswith("GOOD_"):
                    macro_name = this_line.replace('GOOD_','').strip()
                    TT.invoke_macro( macro_name )
                    this_line = "invoked-macro: %s\n" % this_line
                elif this_line.startswith("BAD_"):
                    macro_name = this_line.replace('BAD_','').strip()
                    try:
                        TT.invoke_macro( macro_name )
                        self.fail("This should have failed")
                    except UnitTestException as E:
                        # We expected a name problem here so we are good.
                        this_line = "pass: %s is not a valid macro name\n" % macro_name
                else:
                    self.fail("I'm lost this should not happen")



            # In our actual - we want to have the filename:lineno
            # BUT the filename is abs path.
            # that makes it hard to compare with another test case
            # Your case is: /home/yourname/some/dir/filename.txt
            #   My case is: /home/myname/another/dir/filename.txt
            # SOLUTION: use basename only.
            b_fn = os.path.basename( TT.cur_filename() )
            txt = "%s:%d->%s" % ( b_fn, TT.cur_lineno(), this_line )
            TT.actual.append( txt )
        ln = 0
        tmp = os.path.dirname(afn)
        if not os.path.isdir(tmp):
            os.makedirs(tmp)
        with open( afn, "wt" ) as f:
            # The text in 'actual' - each line contains a terminal newline
            f.write( "".join(TT.actual) )
        # Fetch the expected data.
        with open(efn,"rt") as f:
            expected_lines = f.readlines()

        while (len(TT.actual) > 0) and (len(expected_lines)>0) :
            e = expected_lines.pop(0)
            a = TT.actual.pop(0)
            self.assertEqual(e, a)
        self.assertEqual( len(TT.actual), len(expected_lines) )
        

    def test_a001(self):
        self.simple_test( 'test_a001.txt' )

    def test_a002(self):
        self.simple_test( 'test_a002.txt' )

    def test_a003(self):
        self.simple_test( 'test_a003.txt' )

    def test_a004(self):
        self.simple_test( 'test_a004.txt' )

