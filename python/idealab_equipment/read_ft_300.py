# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 12:48:31 2021

@author: dongting
"""


import socket
import matplotlib.pyplot as plt
import logging
import numpy

def init_ft300(HOST1):
    HOST = HOST1
    PORT = 63351 # The same port as used by the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    return s

def calibrate_ft300(ft300_s):
    import numpy
    calidata1 = ft_300_stream(ft300_s)
    for ii in range(1,1000):       
        calidata1 = numpy.vstack((calidata1,ft_300_stream(ft300_s)))
    calidata = numpy.sum(calidata1,axis=0)/1000
    return calidata

def ft_300_stream(s):      
    data = s.recv(1024)
    encoding = 'utf-8'
    data1 = str(data, encoding)
    data1 = data1.replace("'","")
    data1 = data1.replace("(","")
    data1 = data1.replace(")","\n")
    
    data2 =  data1.split("\n")
    data3= data2[1]
    data4 = data3.split(",")
    ft_data = list(map(float,data4))
    
    # f.write(data)
    # print(ft_data)
    return ft_data

def ft_300_getdata(ft300_s,calidata):
    force_data = ft_300_stream(ft300_s)-calidata
    return force_data
    

HOST = '192.168.1.104' # The remote host
ft300_s = init_ft300(HOST)
calidata = calibrate_ft300(ft300_s)



all_force_data = ft_300_getdata(ft300_s,calidata)

while 1:
    all_force_data = numpy.vstack((all_force_data,ft_300_getdata(ft300_s,calidata)))
    
