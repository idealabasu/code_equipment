# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 14:50:19 2018

@author: daukes
"""

#import ftd2xx
import time
#import ftd2xx.defines as fd
import serial


device = serial.Serial('/dev/ttyUSB0',
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        rtscts=True)

# The Thorlabs protocol description recommends toggeling the RTS pin and resetting the
# input and output buffer. This makes sense, since the internal controller of the Thorlabs
# device does not know what data has reached us of the FTDI RS232 converter.
# Similarly, we do not know the state of the controller input buffer.
# Be toggling the RTS pin, we let the controller know that it should flush its caches.
device.setRTS(1)
time.sleep(0.05)
device.reset_input_buffer()
device.reset_output_buffer()
time.sleep(0.05)
device.setRTS(0)

#device = serial.Serial(
#    port='/dev/ttyUSB0',
#    baudrate=115200,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_ONE,
#    bytesize=serial.EIGHTBITS,
#    rtscts = True
#)

#time.sleep(1)
#device.flush()
#time.sleep(1)
#device.reset_input_buffer()
#device.reset_output_buffer()
#time.sleep(1)
#device.set_input_flow_control(False)
#device.set_output_flow_control(False)
#device.setRTS()
#sn = b'73876440'
#devices = ftd2xx.listDevices() 
#
#if not sn in devices:
#    print("No device found. Exiting...")
#else: 
#    ii = devices.index(sn)
#    print("Initializing device...")
#    device = ftd2xx.open(ii)
#    device.setBaudRate(115200)
##    time.sleep(50/1000)
#    time.sleep(1)
#    device.setDataCharacteristics(fd.BITS_8,fd.STOP_BITS_1,fd.PARITY_NONE)
##    device.setFlowControl()
#    device.purge(fd.PURGE_RX|fd.PURGE_TX)
##    time.sleep(50/1000)
#    time.sleep(1)
#    device.resetDevice()
#    time.sleep(1)
#    device.setFlowControl(fd.FLOW_RTS_CTS,0,0)
#    device.setRts()
#    print(device.getDeviceInfo())
device.write(b'\x05\x00\x00\x00\x11\x01')
time.sleep(.1)
s=device.read(device.inWaiting())
#    for ii in range(10):
#        time.sleep(.1)
#        print(device.getQueueStatus())
#    device.setBitMode()
#    device.setBitMode(255,1) # I think this uses FT_SetBitMode()
#    device.write(b'\01\01')  # relay one on
#    device.write(b'\01\01')  # relay two on
#    device.write(b'\00\00')  # all device off
device.close()

print(s)


