import os
import sys
import threading


sys.path.insert(0,'../../modules')

from harness import TestHarness

my_harness = TestHarness( sys.argv )

EventDone = threading.Event()
def my_expect_code( harness, echild ):
    echild.expect('ABCDEFGHIJKLMNOPQRSTUVWYZ')
    echild.close()
    global EventDone
    EventDone.set()
    # Fall off end of this thread and exit this thread

my_harness.build_testapp()
my_harness.flash_testapp()
my_harness.background_expect( my_expect_code )
my_harness.power_cycle_board()
# Wait at most 5 seconds
EventDone.wait(5.0)

print("Success")
sys.exit(0)



