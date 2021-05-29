# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:51:13 2021

@author: dongting
"""

"""
Before you get started:
install command expert from https://www.keysight.com/us/en/lib/software-detail/computer-software/command-expert-downloads-2151326.html

After that, connect to the device, in our lab it's 34461A
Go to MEAsure, select the value you want to measure, here I select CAPactiance
Create a command, here I set range: Use:parameter, Name: range, Value: MAXimum
resolution: Use:parameter, Name: resolution, Value: DEFault
capactiance: Use:parameter, Name: range, Value: Clicking Add Step & Execute 
Then add step

Now, at the buttom, you can see a second sequence

On the GUI, Select: File-> Export Sequence-> Language: Python with calls to PyVisa
Copy the code it genetated with the following modification:
change> import visa to import pyvisa as visa
change> range to range1, because it will conflict with range in python

You can also change the range to the Parameter in Command Reference, remeber to match with your circuit!

Now, modify the code as following.

IMPORTANT: I know its not consistent with the offical toturial/help from keysight command expert, which requires you to save the sequence and open using os command
But this method is almost the same, we just need the correct rm_address and query_ascii_values generated from this app.

For more details, please check pyvisa documents

"""

# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:51:13 2021

@author: dongting
"""
    
import pyvisa as visa
import time
import numpy
import matplotlib.pyplot as plt
# start of Untitled

range1='1 nF'
resolution='DEFault'

rm = visa.ResourceManager()
v34461A = rm.open_resource('USB0::0x2A8D::0x1301::MY53226596::0::INSTR')

time_a = time.time()

temp_values = v34461A.query_ascii_values(':MEASure:CAPacitance? %s,%s' % (range1, resolution))
capacitance1 = temp_values[0]

while True:   
    temp_values = v34461A.query_ascii_values(':MEASure:CAPacitance? %s,%s' % (range1, resolution))
    capacitance1 = numpy.append(capacitance1,temp_values[0])
    # print(capacitance)

plt.plot(capacitance1)

v34461A.close()
rm.close()


