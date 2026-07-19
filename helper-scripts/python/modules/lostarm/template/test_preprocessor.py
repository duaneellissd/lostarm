import os
import unittest
from lostarm.template.preprocessor import PreProcessor

class TemplateTester( PreProcessor ):
    def __init__(self):
        pass

    def parent_hook(self, text) -> tuple[bool,str]:
        return super().parent_hook(text)

def get_filename( is_in : bool, fn :str ):
    tmp = os.path.abspath(__file__)
    tmp = os.path.dirname(tmp)
    if is_in:
        tmp = os.path.join( tmp, 'test-in', 'preprocessor', fn )
    else:
        tmp = os.path.join( tmp, 'test-out', 'preprocessor', fn )
    return tmp


class TestPreProcessor(unittest.TestCase):

    def simple_test(self, fn : str ):
        # This tests includes
        ifn = get_filename( True, fn )
        ofn = get_filename( False, fn )
        tt = TemplateTester()
        tt.open(ifn)
        with open(ofn,"rt") as f:
            expected_lines = f.readlines()
        actual = []
        done = False
        while not done:
            try:
                actual.append( tt.next_preprocessed_line() )
            except EOFError:
                done =True
        ln = 0
        while (len(actual) > 0) and (len(expected_lines)>0) :
            e = expected_lines.pop(0)
            a = actual.pop(0)
            self.assertEqual(e, a)
        self.assertEqual( len(actual), len(expected_lines) )
        

    def test_a001(self):
