import os
import sys
import argparse

import unittest

import pexpect
import time

EXENAME=None

class test(unittest.TestCase):
    def test_port_timer(self):
        times = []
        times.append( time.time() )
        global EXENAME
        print("EXEC: %s" % EXENAME )
        child = pexpect.spawn( EXENAME )
        line1 = child.readline().decode('utf-8')
        print("Line1 = %s" % line1)
        self.assertTrue( line1.startswith('NOW') )
        
        line2 = child.readline().decode('utf-8')
        print("Line2: %s" % line2 )
        self.assertTrue( line2.startswith('NOW') )
        t2 = float( line2[3:] )/1000000.0
        time.sleep(1.25)
        line3 = child.readline().decode('utf-8')
        print("Line3 %s" % line3 )
        self.assertTrue( line3.startswith('NOW') )
        t3 = float( line3[3:] )/1000000.0
        tdelta = t3 - t2
        
        # Epsilon test is +/- 0.1 seconds
        print("START: %f, END: %f, DELTA: %f\n" % ( t2,t3,tdelta))
        self.assertTrue( (tdelta >= 0.9) )
        self.assertTrue( (tdelta < 1.1 ) )
                          
        
        print("Success!\n");



        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exe',help='testapp')
    args = parser.parse_args()
    EXENAME = args.exe
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
    unittest.TextTestRunner().run(suite)
    
