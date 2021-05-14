import numpy as np
import socket
import time
import os
import datetime

def Init_Ati_Sensor():
    try:
        rospy.loginfo("Initilizing ati sensor")
    except:
        print("Initilizing ati sensor")
    global TCP_IP, TCP_PORT, BUFFER_SIZE, order
    TCP_IP = "192.168.1.122"
    TCP_PORT = 49152
    BUFFER_SIZE = 1024
    order = 'big'
    try:
        rospy.loginfo("Start connection to "+TCP_IP)
    except:
        print("Start connection to "+TCP_IP)
    global message
    message = b''
    message  += (0x1234).to_bytes(2,byteorder=order,signed=False)
    message  += (2).to_bytes(2,order)
    message  += (1).to_bytes(4,order)
#    message = b'\x124\x00\x02\x00\x00\x00\x01'
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    s.connect((TCP_IP, TCP_PORT))
    try:
        rospy.loginfo("Sensor connected")
    except:
        print("Sensor connected")

def extract_raw(packet):
    raw = []
    for ii in range(6):
        byte = packet[12+ii*4:12+ii*4+4]
        value = int.from_bytes(byte,byteorder=order,signed=True)
        raw.append(value)
    return raw
   
def extract_scaling(packet):
    raw = []
    for ii in range(6):
        byte = packet[ii+2:ii+4]
        value = int.from_bytes(byte,byteorder=order,signed=False)
        raw.append(value)
    return raw

def Calibrate_Ati_Sensor():

#    try:
#        rospy.loginfo("Calibrating ati sensor")  
#    except:
#        print("Calibrating ati sensor") 
    s.connect((TCP_IP, TCP_PORT))
    counts_per_unit = np.array([1000000]*3+[1000000]*3)
    global calib_data
    calib_data = np.zeros([1,6])
    for j in range(1,1000):
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        data2 = np.array(extract_raw(data))
        scaled_data = data2/counts_per_unit
        calib_data = calib_data + scaled_data
    calib_data = calib_data/1000
#    try:
#        rospy.loginfo("Calibration finished")
#        rospy.loginfo("Calibration Result"+np.array2string(calib_data))
#    except:
#        print("Calibration finished")
#        print("Calibration Result"+np.array2string(calib_data))
		
def get_data():
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    data2 = np.array(extract_raw(data))
    ati_data = data2/counts_per_unit
    return ati_data

if name == main
    try:
        Init_Ati_Sensor()
    except:
        Init_Ati_Sensor()
        time.sleep(10)
        Init_Ati_Sensor()
    while 1:
        ft_data =get_data()-calib_data
        print(ft_data)