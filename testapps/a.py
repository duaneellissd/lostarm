
import random

random.seed( 0xdeadbeef )

for y in range(0,100):
    x=random.randint(-5,0x7fffffff)
    print("x=%d 0x%08x" % (x,x))
    
