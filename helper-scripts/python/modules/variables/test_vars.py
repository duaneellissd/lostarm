from variables import Variables

import unittest

class VarTestCase( unittest.TestCase ):
    def create(self):
        tmp = Variables()
        tmp.add_variable("DOG","WALTER")
        tmp.add_variable("CAT","GARFIELD")
        return tmp
    
    def test_basic(self):
        dut = self.create()
        result = dut.resolve("${DOG}")
        self.assertEqual("WALTER",result)
        print("SUCCESS")
    
    def test_function( self ):
        dut = self.create()
        result = dut.resolve("${${str.upper(dog)}}")
        self.assertEqual("WALTER",result)
        print("SUCCESS")

        
