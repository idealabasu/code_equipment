"""
Please visit the following link for python3 compatible version of the code 
https://github.com/jpunkt/bkp879b
this device is relative easy to use
here is an example to read capacitance on 'com5'
"""
import bkp879b
instrument = bkp879b.connect("COM5")
instrument.set_primary('C')

instrument.auto_fetch()

import time
time_a = time.time()
for ii in range(0,50):
    print(instrument.fetch())
print(1/50*(time.time()-time_a))
