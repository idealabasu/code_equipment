# for ur5e use the following version  of urx: https://github.com/jkur/python-urx/tree/SW3.5/urx
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 10:17:28 2021

@author: dongting
"""
import numpy
import socket
import time
import os
import datetime
import matplotlib.pyplot as plt
import urx
import serial
import math
import yaml
import logging
import time
import natnet
import serial
from mpl_toolkits import mplot3d
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import butter,filtfilt

def Init_ur5(ur5_port):
    try:
        tcp = ((0,0,0,0,0,0))
        payload_m = 1
        payload_location = (0,0,0.5)    
        ur5 = urx.Robot(ur5_port)
        ur5.set_tcp(tcp)
        ur5.set_payload(payload_m, payload_location)
        print("Connected to Ur5")
    except:
        print("Can not connect, check connection and try again")             
        ur5 = None
    return ur5

def move_ur5(ur5,moving_vector,v,a,wait=False):
    current_pose = ur5.get_pose()
    current_pose.pos[:] += moving_vector
    ur5.movel(current_pose,vel=v,acc=a,wait=wait)


def Init_Ati_Sensor(TCP_IP):
    import socket
    print("Initilizing ati sensor")
    # global TCP_IP, TCP_PORT, BUFFER_SIZE, order

    print("Start connection to "+TCP_IP)
    # global message
    message = b''
    message  += (0x1234).to_bytes(2,byteorder=order,signed=False)
    message  += (2).to_bytes(2,order)
    message  += (1).to_bytes(4,order)
#    message = b'\x124\x00\x02\x00\x00\x00\x01'
    # global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    s.connect((TCP_IP, TCP_PORT))
    print("Sensor connected")
    return s,message

def extract_raw(packet):
    import socket
    raw = []
    for ii in range(6):
        byte = packet[12+ii*4:12+ii*4+4]
        value = int.from_bytes(byte,byteorder=order,signed=True)
        raw.append(value)
    return raw
   
def extract_scaling(packet):
    import socket
    raw = []
    for ii in range(6):
        byte = packet[ii+2:ii+4]
        value = int.from_bytes(byte,byteorder=order,signed=False)
        raw.append(value)
    return raw

def Calibrate_Ati_Sensor(s,TCP_IP,message): 
    import socket
    import numpy as np
    s.connect((TCP_IP, TCP_PORT))
    # global calib_data
    calib_data = np.zeros([1,6])
    for j in range(0,3000):
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        data2 = np.array(extract_raw(data))
        scaled_data = data2/counts_per_unit
        calib_data = calib_data + scaled_data
    calib_data = calib_data/3000
    return calib_data
		
def get_data(s,message):
    import numpy as np
    import socket
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    data2 = np.array(extract_raw(data))
    ati_data = data2/counts_per_unit
    return ati_data

def butter_lowpass_filter(data, cutoff, fs, order):
    from scipy.signal import butter,filtfilt
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


ati_port = "192.168.1.122"
ur5_port = "192.168.1.104"

if ur5_port == "192.168.1.104":
    moving_vector_left = numpy.array((0.001,0.001,0))*math.sqrt(2)/2
    moving_vector_right = -numpy.array((0.001,0.001,0))*math.sqrt(2)/2
    moving_vector_forward = numpy.array((0.001,-0.001,0))*math.sqrt(2)/2
    moving_vector_backward = numpy.array((-0.001,0.001,0))*math.sqrt(2)/2
    moving_vector_up = numpy.array((0,0,0.001))
    moving_vector_down = numpy.array((0,0,-0.001))

if ur5_port == "192.168.1.103":
    moving_vector_left = numpy.array((0.001,0,0))
    moving_vector_right = numpy.array((-0.001,0,0))
    moving_vector_forward = numpy.array((0,-0.001,0))
    moving_vector_backward = numpy.array((0,0.001,0))
    moving_vector_up = numpy.array((0,0,0.001))
    moving_vector_down = numpy.array((0,0,-0.001))

counts_per_unit = numpy.array([1000000]*3+[1000000]*3)
TCP_PORT = 49152
BUFFER_SIZE = 1024
order = 'big'


ati_gamma,message = Init_Ati_Sensor(ati_port)
calib_data = Calibrate_Ati_Sensor(ati_gamma,ati_port,message)

ur5 = Init_ur5(ur5_port)

data_size = 50000
depth = 15
distance = 100
angle = 0
from math import pi
mounting_angle= pi/12

force_data = numpy.zeros([data_size,10])  

time_a = time.time()

move_ur5(ur5,moving_vector_down*depth,1e-3,0.1,wait=False)
initial_pose = ur5.get_pos()[:]

for num in range(0,data_size):
    time_b = time.time()-time_a
    ft_data =get_data(ati_gamma,message)-calib_data
    position_data = ur5.get_pos()[:]-initial_pose
    current_data= numpy.append(time_b,ft_data)
    current_data = numpy.append(current_data,position_data)
    force_data[num,:] = current_data
    
    if num == 10000:
        move_ur5(ur5,moving_vector_backward*distance,1e-3,0.1,wait=False)
    if num == 40000:
        move_ur5(ur5,moving_vector_up*depth,1e-3,0.1,wait=False)
    time.sleep(0.00001)
    # time.sleep(0.0015)

move_ur5(ur5,moving_vector_forward*distance,1e-3,0.1,wait=False)

# data processing

T = force_data[-1,0]-force_data[0,0]     # Sample Period
fs = data_size/force_data[-1,0]     # sample rate, Hz
cutoff = 0.5   # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 2       # sin wave can be approx represented as quadratic
n = int(T * fs) # total number of samples

# Calculate the distance according to the mounting angles

#zero the distance

transformed_force_x = force_data[:,1]*numpy.cos(mounting_angle)-force_data[:,2]*numpy.sin(mounting_angle)
transformed_force_y = force_data[:,2]*numpy.cos(mounting_angle)+force_data[:,1]*numpy.sin(mounting_angle)

# filtered_force_Fx = butter_lowpass_filter(transformed_force_x, cutoff, fs, order)
# filtered_force_Fy = butter_lowpass_filter(transformed_force_y, cutoff, fs, order)
# filtered_force_Fz = butter_lowpass_filter(force_data[:,3], cutoff, fs, order)
# filtered_force_Tx = butter_lowpass_filter(force_data[:,4], cutoff, fs, order)
# filtered_force_Ty = butter_lowpass_filter(force_data[:,5], cutoff, fs, order)
# filtered_force_Tz = butter_lowpass_filter(force_data[:,6], cutoff, fs, order)

force_data[:,1] = butter_lowpass_filter(transformed_force_x, cutoff, fs, order)
force_data[:,2] = butter_lowpass_filter(transformed_force_y, cutoff, fs, order)
force_data[:,3] = butter_lowpass_filter(force_data[:,3], cutoff, fs, order)
force_data[:,4] = butter_lowpass_filter(force_data[:,4], cutoff, fs, order)
force_data[:,5] = butter_lowpass_filter(force_data[:,5], cutoff, fs, order)
force_data[:,6] = butter_lowpass_filter(force_data[:,6], cutoff, fs, order)


plt.figure()
plt.plot(force_data[:,0],force_data[:,1:4])


plt.figure()
plt.plot(force_data[:,0],force_data[:,7])
plt.plot(force_data[:,0],force_data[:,-1])


numpy.savetxt(f'0424_drag_depth_{depth:01d}_angle_{angle:01d}.csv', force_data, fmt='%.18e', delimiter=',', newline='\n')
