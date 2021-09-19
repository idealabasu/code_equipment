# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 20:11:37 2021

@author: dongting
"""

# Need to work with arduino code in folder Arudino

import serial
import time


def Initial_Arduino():
    global Ard
    Ard = serial.Serial('COM8',115200,timeout=0.1)
    time.sleep(2)
    Ard.flush()
    Ard.flushOutput()
    Ard.flushInput()
    return Ard

step_motor = Initial_Arduino()

max_n = round(90/(360/400))
S_data = 1


for i in range (0,max_n):
    xn = str(S_data).encode()
    xn += "\n".encode()
    step_motor.write(xn)
    is_there = 0
    while is_there == 0:
        z = step_motor.readline()
        try:
            zint = int(z.decode())
        except:
            z = 4
        if zint == 5:
            is_there = 1
        else:
            is_there = 0