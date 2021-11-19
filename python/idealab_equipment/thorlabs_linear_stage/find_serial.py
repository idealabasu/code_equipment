#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:47:12 2020

@author: idealab
"""

#import usb
#import serial
import serial.tools.list_ports as lp
import serial.tools.list_ports_common as lpc


all_ports = lp.comports()
my_filter = lambda port: 'thorlabs' in port.manufacturer.lower()
all_ports = lp.comports()
my_ports = [port for port in all_ports if my_filter(port)]
        

#usb_devices = usb.core.find(find_all=True)
#for device in usb_devices:
#    if device.bDeviceClass!=9:
#        try:
#            print(device.manufacturer)
#        except ValueError:
#            device._langids = (1033,)


for port in my_ports :
    print(port.device,port.serial_number)
    

wincomports = ['COM'+str(item) for item in range(256)]

for port in wincomports:
    p = lpc.ListPortInfo(port)
    print(p.manufacturer)