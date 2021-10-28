# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 08:36:13 2020

@author: danaukes
"""

import numpy
import numpy as np
import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.stream_writers import AnalogMultiChannelWriter
from nidaqmx import constants
import time

import roslibpy

daq_read_task = nidaqmx.Task()
daq_calibration_task = nidaqmx.Task()
daq_sample_rate = 50
chans_in = 4
buffer_in_size = 100
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration
# Initialize data placeholders
buffer_in = np.zeros((chans_in, buffer_in_size))
daq_data = np.zeros((chans_in, 1))  # will contain a first column with zeros but that's fine

client = roslibpy.Ros(host='192.168.1.164', port=9090)
client.run()

talker = roslibpy.Topic(client, '/ni_daq_data', 'ati_nano/write')

def configure_daq():
    sample_rate = daq_sample_rate
    daq_read_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan("Dev1/ai1", max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan("Dev1/ai2", max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan("Dev1/ai3", max_val=10, min_val=-10)
    daq_read_task.timing.cfg_samp_clk_timing(rate=sample_rate, sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=buffer_in_size_cfg)

def reading_task_callback(task_idx, event_type, num_samples, callback_data):  # bufsize_callback is passed to num_samples
    global daq_data
    global buffer_in

    if running:
        # # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
        # # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
        buffer_in = np.zeros((chans_in, num_samples))  # double definition ???
        reader.read_many_sample(buffer_in, num_samples, timeout=constants.WAIT_INFINITELY)
        # talker.publish(roslibpy.Message({'data': str(buffer_in)}))
        talker.publish(roslibpy.Message({'fx':0,'fy':0,'fz':0,'tx':0,'ty':0,'tz':0}))
        # talker.publish(roslibpy.Message({'fx':'0.0','fy':'0.0','fz':'0.0','tx':'0.0','ty':'0.0','tz':'0.0'}))
        # talker.publish(roslibpy.Message("['0.0', '0.0', '0.0', '0.0', '0.0', '0.0']"))
        # daq_data = np.append(daq_data,buffer_in,axis=1)
        # # daq_data =  np.concatenate(daq_data, buffer_in, axis = 1)  # appends buffered data to total variable data
        print('samples:',num_samples)

    return 0  # Absolutely needed for this callback to be well defined (see nidaqmx doc).
    
def daq_acquisition():
    global running
    global reader
    global daq_data
    running = True
    reader = AnalogMultiChannelReader(daq_read_task.in_stream)
    daq_read_task.register_every_n_samples_acquired_into_buffer_event(bufsize_callback, reading_task_callback)
    

def daq_calibration():
    daq_calib_data = daq_calibration_task.read()
    return daq_calib_data

print("Start load cell calibration, please lift up the object")
# time.sleep(5)
print("Calibration start")
configure_daq()
tic = time.time()
toc = time.time()
daq_force = []
daq_calibration_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan("Dev1/ai1", max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan("Dev1/ai2", max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan("Dev1/ai3", max_val=10, min_val=-10)
while toc - tic <= 1:
    daq_force.append(daq_calibration())
    toc = time.time()
daq_force = np.array(daq_force)
daq_calibration = np.mean(daq_force,axis=1)
daq_calibration_task.close()
print("Calibration finished")


daq_acquisition()


    
#     daq_read_task.start()
#     daq_read_task.stop()
   
#     talker.publish(roslibpy.Message({'data': 'Hello World!'}))
#     print('Sending message...')
#     time.sleep(1)

# try:
daq_read_task.start()

try:
    while client.is_connected:
        time.sleep(1)

except KeyboardInterrupt:
    pass

daq_read_task.stop()
daq_read_task.close()
talker.unadvertise()
client.terminate()
    