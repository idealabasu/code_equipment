# -*- coding: utf-8 -*-
"""
Created on Sat May 29 15:51:13 2021

@author: dongting
"""
    
import pyvisa as visa
import time
import numpy
import matplotlib.pyplot as plt
import pyfirmata


# Configure Arduino
board = pyfirmata.Arduino('COM7')

it = pyfirmata.util.Iterator(board)
it.start()

dis_pin = 1
board.analog[dis_pin].mode = pyfirmata.INPUT

force_pin = 2
board.analog[force_pin].mode = pyfirmata.INPUT

# End Configure Arduino

#configure Keysight
range1='1 nF'
resolution='DEFault'

rm = visa.ResourceManager()
v34461A = rm.open_resource('USB0::0x2A8D::0x1301::MY53226596::0::INSTR')

# v34461A.set_visa_attribute(visa.constants.VI_ATTR_ASRL_BAUD, 1073676321)


# End configure Keysight

# Init data collection

time_a = time.time()

raw_dis = board.analog[dis_pin].read()
raw_force = board.analog[force_pin].read()

temp_values = v34461A.query_ascii_values(':MEASure:CAPacitance? %s,%s' % (range1, resolution))
capacitance1 = temp_values[0]

time_b = time.time() - time_a
dis_cap_force = [time_b,raw_dis,raw_force,capacitance1]
# End init data collection

print("Start!")


try: 
    while True:
        raw_dis = board.analog[dis_pin].read()
        raw_force = board.analog[force_pin].read()
        
        temp_values = v34461A.query_ascii_values(':MEASure:CAPacitance? %s,%s' % (range1, resolution))
        capacitance1 = temp_values[0]
        
        time_b = time.time() - time_a
        dis_cap_force = numpy.vstack([dis_cap_force,[time_b,raw_dis,raw_force,capacitance1]])
    
except KeyboardInterrupt:
    
    avg_sampleRate = len( dis_cap_force[:,0]) / (dis_cap_force[-1,0]-dis_cap_force[0,0])
    print(str(avg_sampleRate)+"Hz")   


    plt.plot(dis_cap_force[:,-1]*1e9)
    plt.plot(dis_cap_force[:,1:3])

    v34461A.close()
    rm.close()

