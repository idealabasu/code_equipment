# -*- coding: utf-8 -*-
'''
Created on Thu Jun 30 09:19:11 2022

@author: daukes
'''

import numpy
import nidaqmx
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.stream_writers import AnalogMultiChannelWriter
from nidaqmx import constants
import time
import logging
import roslibpy

daq_read_task = nidaqmx.Task()
daq_calibration_task = nidaqmx.Task()
daq_sample_rate = 1
chans_in = 4
buffer_in_size = 1
bufsize_callback = buffer_in_size
buffer_in_size_cfg = round(buffer_in_size * 1)  # clock configuration


buffer_in = numpy.zeros((chans_in, buffer_in_size))
daq_data = numpy.zeros((chans_in, 1))  # will contain a first column with zeros but that's fine

# add debug info. Can be comment out 
fmt = '%(asctime)s %(levelname)8s: %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG)
log = logging.getLogger(__name__)
# End debug info

client = roslibpy.Ros(host='192.168.1.164', port=9090)
client.on_ready(lambda: log.info('On ready has been triggered'))
client.run()

talker = roslibpy.Topic(client, '/ni_daq', 'ni_daq/ni_4_forces')



def configure_daq():
    sample_rate = daq_sample_rate
    daq_read_task.ai_channels.add_ai_voltage_chan('Dev1/ai0', max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan('Dev1/ai1', max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan('Dev1/ai2', max_val=10, min_val=-10)
    daq_read_task.ai_channels.add_ai_voltage_chan('Dev1/ai3', max_val=10, min_val=-10)
    daq_read_task.timing.cfg_samp_clk_timing(rate=sample_rate, sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS, samps_per_chan=buffer_in_size_cfg)


def reading_task_callback(task_idx, event_type, num_samples, callback_data):  # bufsize_callback is passed to num_samples
    global seq    
    global daq_data
    global buffer_inwe

    if running:
        seq+=1
        # # It may be wiser to read slightly more than num_samples here, to make sure one does not miss any sample,
        # # see: https://documentation.help/NI-DAQmx-Key-Concepts/contCAcqGen.html
        buffer_in = numpy.zeros((chans_in, num_samples))  # double definition ???
        reader.read_many_sample(buffer_in, num_samples, timeout=constants.WAIT_INFINITELY)
        daq_data = numpy.append(daq_data,buffer_in,axis=1)
        header1 = roslibpy.Header(frame_id='', seq=seq, stamp=roslibpy.Time.now())
        talker.publish(roslibpy.Message({'c1':buffer_in[0].tolist(),'c2':buffer_in[1].tolist(),'c3':buffer_in[2].tolist(),'c4':buffer_in[3].tolist()}))
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



configure_daq()

tic = time.time()
toc = time.time()

daq_force = []
daq_calibration_task.ai_channels.add_ai_voltage_chan('Dev1/ai0', max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan('Dev1/ai1', max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan('Dev1/ai2', max_val=10, min_val=-10)
daq_calibration_task.ai_channels.add_ai_voltage_chan('Dev1/ai3', max_val=10, min_val=-10)

while toc - tic <= 1:
    daq_force.append(daq_calibration())
    toc = time.time()
    
daq_force = numpy.array(daq_force)
daq_calibration = numpy.mean(daq_force)
daq_calibration_task.close()

daq_acquisition()
seq=0
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
