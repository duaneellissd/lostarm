from lostarm.variables import Variables, VarError
import os
import inspect
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

    def test_two(self):
        dut = self.create()
        result = dut.resolve("There is a ${DOG} and ${CAT} here")
        print("result: %s" % result)
        self.assertEqual("There is a WALTER and GARFIELD here",result )
    
    def test_function( self ):
        dut = self.create()
        result = dut.resolve("${${str.upper(dog)}}")
        self.assertEqual("WALTER",result)
        print("SUCCESS")

    def _create_test_v(self):
        v = Variables()
        # Simple replacement.
        v.add('dog3', 'walter')
        v.add('dog1', 'shatzi')
        v.add('dog2', 'dolly')
        v.add("DOG", "${str.upper(${dog1})}")
        # create a loop
        v.add("A", "${B}")
        v.add("B", "${C}")
        v.add("C", "${A}")
        return v

    def _standard_case(self,input_text, expected_text):
        DUT = self._create_test_v()
        answer = DUT.resolve(input_text)
        assert (answer == expected_text)
        frame = inspect.currentframe().f_back
        print("Success: %s" % frame.f_code.co_name)

    def _expect_error(self,text, errcode):
        DUT = self._create_test_v()
        DUT.just_exit = False
        try:
            DUT.resolve(text)
            # should have asserted
            assert (False)
        except VarError as E:
            assert (E.typecode == errcode)
        # All is well
        frame = inspect.currentframe().f_back
        print("Success: %s" % frame.f_code.co_name)

    def _test_case1(self):
        '''Simple...'''
        self._standard_case("${dog3}", "walter")

    def _test_case2(self):
        ''' Nested.. '''
        DUT = self._create_test_v()
        DUT.replace("C", "${dog3}")
        answer = DUT.resolve("${A}")
        assert (answer == 'walter')
        print("success: _test_case2")

    def _test_case3(self):
        self._expect_error("${cat}", VarError.UNDEF_VAR)

    def _test_case4(self):
        self._expect_error("${A}", VarError.RECURSION)

    def _test_case5(self):
        self._standard_case("my dogs name is: ${dog3}", 'my dogs name is: walter')

    def _test_case6(self):
        self._standard_case("${dog3} is my dogs name", 'walter is my dogs name')

    def _test_case7(self):
        self._standard_case("first ${dog1} second: ${dog2} third: ${dog3} today",
                       "first shatzi second: dolly third: walter today")

    def _test_case8(self):
        self._expect_error("var ${dog without close", VarError.SYNTAX)

    def _test_case9(self):
        self._standard_case("${dog1} ${dog2} ${dog3}", "shatzi dolly walter")

    def _test_case10(self):
        self._standard_case("${DOG}", "SHATZI")

    def _test_case11(self):
        tmp = os.getcwd()
        self._standard_case("${os.getcwd()}", tmp)
        expect = "before %s after" % tmp
        self._standard_case("before ${os.getcwd()} after", expect)

    def _test_case12(self):
        tmp = "dog %s cat" % os.getcwd()
        self._standard_case("dog ${os.path.abspath(.)} cat", tmp)

    def _test_case13(self):
        v = Variables()
        v.add_dict(os.environ)
        s = v.resolve("Your HOME dir is ${HOME}")
        print("Result: %s" % s)

    def test_oldway(self):
        """
        Unit test for this module is here.
        """
        self._test_case1()
        self._test_case2()
        self._test_case3()
        self._test_case4()
        self._test_case5()
        self._test_case6()
        self._test_case7()
        self._test_case8()
        self._test_case9()
        self._test_case10()
        self._test_case11()
        self._test_case12()
        self._test_case13()
        print("var selftest complete")

