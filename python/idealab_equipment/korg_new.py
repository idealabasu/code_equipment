#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:24:23 2021

@author: idealab
"""

import mido
from mido import Message
#import rtmidi
#
#i =rtmidi.RtMidiIn()
#i.getPortCount
#i.getPortCount()
#i.openPort(0)
#i.isPortOpen()
#i.getPortName(0)
#i.getMessage()


class Device(object):
    
    def __init__(self):
        channel0 = Channel()
        
        self.events = {}
        self.events[(0,2)] = channel0.update_value_rough
        self.events[(0,14)] = channel0.update_value_fine
    
    def callback(self,message):
        self.message = message
        
        t = self.message.channel, self.message.control
        try:
            self.events[t](message.value)
        except KeyError:
            print(message)

    
    def connect(self):
        names = mido.get_input_names()
        for item in names:
            if 'nanoKONTROL' in item:
                mido_device = mido.open_input(item,callback=self.callback)
                self.mido_device = mido_device
                break
    def receive(self):
        while True:
            self.mido_device.poll()
#        self.mido_device.receive()
        

class Channel(object):
    scaling_fine = .1
    scaling_rough = 1
    
    def __init__(self):
        self.tare_rough = None
        self.tare_fine = None
        self.value_rough = None
        self.value_fine = None
        self.value = 0
    
    def update_value_rough(self,value):
        print(self.value_rough,value)
        if self.tare_rough is None:
            self.tare_rough = value
            self.value_rough = value
        else:
            self.value_rough = value

        self.update_value()

    def update_value_fine(self,value):
        print(self.value_fine,value)
        if self.tare_fine is None:
            self.tare_fine = value
            self.value_fine = value
        else:
            self.value_fine = value
            
        self.update_value()
            
    def update_value(self):
        value = 0
        if self.tare_rough is not None:
            if self.value_rough is not None:
                value += (self.value_rough-self.tare_rough)*self.scaling_rough
        if self.tare_fine is not None:
            if self.value_fine is not None:
                value += (self.value_fine-self.tare_fine)*self.scaling_fine
        self.value = value
        print(value)


#        self.channels = [-1 for item in range(self.num_channels)]

d = Device()
#i.receive()
#print(n)
d.connect()

d.receive()

