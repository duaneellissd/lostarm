import os
import unittest
import glob
import json
import pmake
import shutil

import pmake.json_reader

this_dir = os.path.dirname( os.path.abspath( __file__ ))
test_data_dir=os.path.join( this_dir, "test_data" )
log_dir = os.path.join( this_dir, 'log-output' )
print("Mkdir: %s" % log_dir)
if not os.path.isdir(log_dir):
    os.makedirs( log_dir )    
    
in_files = glob.glob( os.path.join( test_data_dir , "in_*.json" ))
good_files = glob.glob( os.path.join( test_data_dir, "out_*.json" ))
print("todo: %d good tests" % len(good_files))
error_files = glob.glob( os.path.join( test_data_dir, "out_*.error" ) )
print("todo: %d error cases" % len(error_files))


def good_to_in( fn ):
    '''
    Given a filename in the form:  "out_*.json" 
    Transform to: in_*.json
    '''
    dname = os.path.dirname( fn )
    out_fn = os.path.basename( fn )
    # Remove: "out_" from "out_*.json"
    testname = out_fn[4:-5]
    in_fn = "in_%s.json" % testname
    in_fn = os.path.join( dname, in_fn )
    return (in_fn, testname)

def error_to_in( fn ):
    '''
    Given a filename in the form: "out_*.error"
    transform it to: "in_*.json"
    '''
    dname = os.path.dirname( fn )
    out_fn = os.path.basename(fn)
    test_name = out_fn[ 4: -6 ]
    in_fn = "in_%s.json" % test_name
    in_fn = os.path.join( dname, in_fn )
    return (in_fn, test_name )

class JsonTool_Test( unittest.TestCase ):
    def _if_evaulator( self, reader_object, expression_text : str ):
        '''
        The JSON Reader has found an "if( EXPRESSION )" key
        this function needs to evaluate that expression.
        
        The expression could be complex, or it could be simple
        For our TEST purposes we only support 2 types of expressions:
        Exactly the word: "True" or the word "False"
        And nothing else.
        '''
        expression_text = expression_text.strip().upper()
        if expression_text == 'TRUE':
            return True
        if expression_text == 'FALSE':
            return False
        reader_object.parse_error("INVALID_EXPRESSION")

    def _var_define( self, name, value ):
        if not hasattr( self, 'test_vars'):
            self.test_vars = dict()
        self.test_vars[name] = value
        
    def reset_good_test_case( self, good_out_file ):
        in_filename, testname = good_to_in( good_out_file )
        pmake.log_unit_test_restart( log_dir, testname )
        return in_filename, testname

    def reset_error_test_case( self, error_out_file ):
        in_filename, testname = error_to_in( error_out_file )
        pmake.log_unit_test_restart( log_dir, testname )
        return in_filename, testname

    def test_GoodCases( self ):
        '''
        Loop through all known good test cases and execute them
        '''
        if len(good_files) == 0:
            self.fail("No good file test cases?")

        for good_out_filename in good_files:
            self._this_good_test( good_out_filename )
    
    def _this_good_test( self, good_out_filename ):
        '''
        Run this test with this file.

        This makes it easy to debug a specific test
        '''
        print("\nSTART: %s" % good_out_filename )
        in_filename, testname = self.reset_good_test_case( good_out_filename )
        reader = pmake.JsonReader( self._if_evaulator, self._var_define )
        reader.add_include_path( test_data_dir )
        reader.setNoExit()
        result = reader.read_file( in_filename )
        # read the expected result
        with open( good_out_filename, "rt" ) as f:
            txt = f.read()
        # The expected result might have extra white space
        # Or extra newlines, etc - by converting to JSON and FROM json
        # We effectively "nomalize" the json data.
        good_dict = json.loads(txt)
        good_text = json.dumps(good_dict,indent=4)
        dut_text = json.dumps( result, indent=4 )
        if good_text == dut_text:
            print(" PASS: %s" % good_out_filename )
            pmake.debug_print(0,"TEST CASE: %s - success" % testname )
            vars_expected = good_dict.get('var-check',None)
            if vars_expected is not None:
                self.assertEqual( len(vars_expected.keys()) , len(self.test_vars.keys()) )
                for k,v in self.test_vars.items():
                    self.assertEqual( vars_expected[k], v )
            return
        else:
            print("FAIL: %s" % good_out_filename )
            print(0,"EXPECTED:\n===============\n%s\n===================\n" % good_text )
            print(0," ACTUAL:\n===============\n%s\n===================\n" % dut_text )
            self.fail("Does not match")

    def test_ErrorCases(self):
        '''
        Loop through all known error test cases and execute them.
        '''
        if len(error_files) == 0:
            print("No error file test cases?")
            return

        for error_out_filename in error_files:
            self._this_error_test( error_out_filename )

    def _this_error_test( self, error_out_filename ):
        '''
        Run this test with this file.

        This makes it easy to debug a specific test
        '''
        print("\nSTART: %s" % error_out_filename )
        in_filename, testname = self.reset_error_test_case( error_out_filename )
        reader = pmake.JsonReader( self._if_evaulator, self._var_define )
        reader.add_include_path( test_data_dir )
        reader.setNoExit()
        try:
            result = reader.read_file( in_filename )
            self.fail( "Expected an exception it did not occur")
        except pmake.json_reader.JsonReader_UnitTestError as E:
            actual_reason = E.short_reason
        print("actual-error REASON: %s" % actual_reason )
        
        # read the expected error
        with open( error_out_filename, "rt" ) as f:
            expected_error = f.read()
        expected_error = expected_error.strip()

        if expected_error == actual_reason:
            print(" PASS: %s" % error_out_filename )
            pmake.debug_print(0,"TEST CASE: %s - success" % testname )
            return
        else:
            self.fail("FAIL: %s expected: %s, got: %s" % (testname, expected_error, actual_reason) )


            
