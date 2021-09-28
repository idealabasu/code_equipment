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


class KorgEvent(object):
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
#        self.message = message
#        self.channel = channel
#        self.control = control
#        self.value = value
#        self.time = time

k = KorgEvent(0,a=1)

def callback(*args,**kwargs):
    global k
#    print(len(args))
    k = KorgEvent(*args,**kwargs)

n = mido.get_input_names()
for item in n:
    if 'nanoKONTROL' in item:
        i = mido.open_input(item,callback=callback)
        break

i.receive()
#print(n)
