# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:49:31 2020

@author: danaukes
"""

import thorlabs_linear_stage.message_dicts as md
#import thorlabs_linear_stage.message_sets as ms
from thorlabs_linear_stage.message import Message
#import thorlabs_linear_stage.apt_types
import thorlabs_linear_stage.apt_data as apt_data

import time

import serial
    
#class BrushlessDCController(object):
#    
#    
#    @classmethod
#    def pos_apt(cls):
#    
#class BBD201(BrushlessDCController):

class NoMessage(Exception):
    pass

class BBD201(object):

    baud_rate = 115200
    dest = 0x11
    mytype = 'serial'
    
    def __init__(self,serial_number):
        self.serial_number = serial_number.encode()
    
    def connect(self):
        if self.mytype =='serial':
            return self.connect_serial()
        else:
            return self.connect_ftdi()
    
    def connect_ftdi(self):
        import ftd2xx
        import ftd2xx.defines as fd
        devices = ftd2xx.listDevices() 
        
        if not self.serial_number in devices:
            print("No device found. Exiting...")
            return None
        else: 
            ii = devices.index(self.serial_number)
            print("Initializing device...")
            device = ftd2xx.open(ii)
            device.setBaudRate(self.baud_rate)
        #    time.sleep(50/1000)
            time.sleep(1)
            device.setDataCharacteristics(fd.BITS_8,fd.STOP_BITS_1,fd.PARITY_NONE)
        #    device.setFlowControl()
            device.purge(fd.PURGE_RX|fd.PURGE_TX)
        #    time.sleep(50/1000)
            time.sleep(1)
            device.resetDevice()
            time.sleep(1)
            device.setFlowControl(fd.FLOW_RTS_CTS,0,0)
            device.setRts()
            print(device.getDeviceInfo())
            self.device = device

    def connect_serial(self):

        device = serial.Serial('/dev/ttyUSB0',
                               baudrate=115200,
                               bytesize=serial.EIGHTBITS,
                               parity=serial.PARITY_NONE,
                               stopbits=serial.STOPBITS_ONE,
                               rtscts=True)
        device.setRTS(1)
        time.sleep(0.05)
        device.reset_input_buffer()
        device.reset_output_buffer()
        time.sleep(0.05)
        device.setRTS(0)
#            print(device.getDeviceInfo())
        self.device = device

    def send_message(self,request):
        self.device.write(request.message)

    def send_message_receive_response(self,request):
        self.device.write(request.message)
        time.sleep(.1)
        message = self.get_messages()
        if message is None:
            raise NoMessage
        return message
        
    def get_messages(self):
        if self.mytype =='serial':
            return self.get_messages_serial()
        else:
            return self.get_messages_ftdi()
    
    def get_messages_ftdi(self):
        l = self.device.getQueueStatus()
        if l>0:
            s=self.device.read(self.device.getQueueStatus())
            response = Message(s)
            response.parse()
            return response
        
    def get_messages_serial(self):
        l = self.device.inWaiting()
        if l>0:
            s=self.device.read(self.device.inWaiting())
            response = Message(s)
            response.parse()
            return response
        
    def info(self):
        request = Message.build(md.message.HW_REQ_INFO,dest = self.dest)
        response = self.send_message_receive_response(request)
        return response

    
#
#    def rack_req_bayused(self,bay):
#        request = Message.build(md.message.RACK_REQ_BAYUSED,dest = self.dest,param1 = bay)
#        response = self.send_message_receive_response(request)
#        return response
#
#



    def close(self):
        self.device.close()
        time.sleep(1)
        del self.device

class LinearStage(object):
    enc_cnt_per_mm = 1
    k_velocity = 1
    k_acceleration = 1
    T = 102.4e-8
    
    def __init__(self,dest,channel,controller):
        self.dest = dest
        self.channel = channel
        self.controller = controller

    def info(self):
        request = Message.build(md.message.HW_REQ_INFO,dest = self.dest)
        response = self.controller.send_message_receive_response(request)
        return response

    def mod_set_chanenablestate(self,value):
        request = Message.build(md.message.MOD_SET_CHANENABLESTATE,dest = self.dest,param1 = self.channel,param2=value)
        response = self.controller.send_message(request)
        return response

    def mod_req_chanenablestate(self,value):
        request = Message.build(md.message.MOD_REQ_CHANENABLESTATE,dest = self.dest,param1 = self.channel,param2=value)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_velparams(self):
        request = Message.build(md.message.MOT_REQ_VELPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_jogparams(self):
        request = Message.build(md.message.MOT_REQ_JOGPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_genmoveparams(self):
        request = Message.build(md.message.MOT_REQ_GENMOVEPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_moverelparams(self):
        request = Message.build(md.message.MOT_REQ_MOVERELPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_moveabsparams(self):
        request = Message.build(md.message.MOT_REQ_MOVEABSPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_homeparams(self):
        request = Message.build(md.message.MOT_REQ_HOMEPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response
#
#    def mot_req_powerparams(self):
#        request = Message.build(md.message.MOT_REQ_POWERPARAMS,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response

    def mot_req_limswitchparams(self):
        request = Message.build(md.message.MOT_REQ_LIMSWITCHPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

#    def mot_req_bowindex(self):
#        request = Message.build(md.message.MOT_REQ_BOWINDEX,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response

    def mot_req_dcpidparams(self):
        request = Message.build(md.message.MOT_REQ_DCPIDPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

#    def mot_req_avmodes(self):
#        request = Message.build(md.message.MOT_REQ_AVMODES,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response
#
#    def mot_req_potparams(self):
#        request = Message.build(md.message.MOT_REQ_POTPARAMS,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response

#    def mot_req_buttonparams(self):
#        request = Message.build(md.message.MOT_REQ_BUTTONPARAMS,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response

    def mot_req_pmdpositionloopparams(self):
        request = Message.build(md.message.MOT_REQ_PMDPOSITIONLOOPPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_pmdmotoroutputparams(self):
        request = Message.build(md.message.MOT_REQ_PMDMOTOROUTPUTPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_pmdtracksettleparams(self):
        request = Message.build(md.message.MOT_REQ_PMDTRACKSETTLEPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response
    def mot_req_pmdprofilemodeparams(self):
        request = Message.build(md.message.MOT_REQ_PMDPROFILEMODEPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response
    def mot_req_pmdjoystickparams(self):
        request = Message.build(md.message.MOT_REQ_PMDJOYSTICKPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_pmdcurrentloopparams(self):
        request = Message.build(md.message.MOT_REQ_PMDCURRENTLOOPPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

    def mot_req_pmdsettledcurrentloopparams(self):
        request = Message.build(md.message.MOT_REQ_PMDSETTLEDCURRENTLOOPPARAMS,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response

#    def mot_req_pmdstageaxisparams(self):
#        request = Message.build(md.message.MOT_GET_PMDSTAGEAXISPARAMS,dest = self.dest,param1 = self.channel)
#        response = self.controller.send_message_receive_response(request)
#        return response

    def mot_req_statusupdate(self):
        request = Message.build(md.message.MOT_REQ_STATUSUPDATE,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response
    

    def mot_move_home(self,blocking=True):
        request = Message.build(md.message.MOT_MOVE_HOME,dest = self.dest)
        self.controller.send_message(request)

        if blocking:
            received = False
            while not received:
                response = self.controller.get_messages()
                if response is not None:
                    if response.msg_id=='MOT_MOVE_HOMED':
                        received = True
                time.sleep(.05)
            print(response.msg_id)        
            
            return response
        

    def mot_move_relative(self,data,blocking=True):
        request = Message.build(md.message.MOT_MOVE_RELATIVE,dest = self.dest,data = data)
        self.controller.send_message(request)
        
        if blocking:
            received = False
            while not received:
                response = self.controller.get_messages()
                if response is not None:
                    if response.msg_id=='MOT_MOVE_COMPLETED':
                        received = True
                time.sleep(.05)
            print(response.msg_id)
            
            return response

    def mot_move_absolute(self,data,blocking=True):
        request = Message.build(md.message.MOT_MOVE_ABSOLUTE,dest = self.dest,data = data)
        self.controller.send_message(request)
        
        if blocking:
            received = False
            while not received:
                response = self.controller.get_messages()
                if response is not None:
                    if response.msg_id=='MOT_MOVE_COMPLETED':
                        received = True
                time.sleep(.05)
            print(response.msg_id)
            
            return response
    
    
    def mot_move_jog(self,blocking=True):
        request = Message.build(md.message.MOT_MOVE_JOG,dest = self.dest)
        self.controller.send_message(request)
        
        if blocking:
            received = False
            while not received:
                response = self.controller.get_messages()
                if response is not None:
                    if response.msg_id=='MOT_MOVE_COMPLETED':
                        received = True
                time.sleep(.05)
            print(response.msg_id)
            
            return response
    
    def mot_move_velocity(self):
        request = Message.build(md.message.MOT_MOVE_VELOCITY,dest = self.dest)
        self.controller.send_message(request)
        
#        if blocking:
#            received = False
#            while not received:
#                response = self.controller.get_messages()
#                if response is not None:
#                    if response.msg_id=='MOT_MOVE_COMPLETED':
#                        received = True
#                time.sleep(.05)
#            print(response.msg_id)
#            
#            return response    

    def mot_move_stop(self,blocking=True):
        request = Message.build(md.message.MOT_MOVE_STOP,dest = self.dest)
        self.controller.send_message(request)
        
        if blocking:
            received = False
            while not received:
                response = self.controller.get_messages()
                if response is not None:
                    if response.msg_id=='MOT_MOVE_STOPPED':
                        received = True
                time.sleep(.05)
            print(response.msg_id)
            
            return response    
    
    def mot_req_poscounter(self):
        request = Message.build(md.message.MOT_REQ_POSCOUNTER,dest = self.dest,param1 = self.channel)
        response = self.controller.send_message_receive_response(request)
        return response
        
    def save_parameters(self,filename='current_parameters.txt'):
        rc = self.controller.info()
        r1 = self.info()
    #    #r2 = controller.query_channel(0x22)
    #    #r = controller.mod_set_chanenablestate(0x21,0x02)
    #    #r = controller.mod_set_chanenablestate(0x21,0x01)
    #    #r3 = controller.move_home(0x21)
    #    r1 = controller.rack_req_bayused(0x00)
    #    r2 = controller.rack_req_bayused(0x01)
    #    r3 = controller.rack_req_bayused(0x02)
        r3 = self.mot_req_velparams()
        r4 = self.mot_req_jogparams()
        r5 = self.mot_req_genmoveparams()
        r6 = self.mot_req_moverelparams()
        r7 = self.mot_req_moveabsparams()
        r8 = self.mot_req_homeparams()
    #    r9 = self.mot_req_powerparams()
        r10 = self.mot_req_limswitchparams()
    #    r11 = self.mot_req_bowindex()
    #    r12 = self.mot_req_dcpidparams()
    #    r13 = self.mot_req_avmodes()
    #    r14 = self.mot_req_potparams()
    #    r15 = self.mot_req_buttonparams()
        r16 = self.mot_req_pmdpositionloopparams()
        r17 = self.mot_req_pmdmotoroutputparams()
        r18 = self.mot_req_pmdtracksettleparams()
        r19 = self.mot_req_pmdprofilemodeparams()
        r20 = self.mot_req_pmdjoystickparams()
        r21 = self.mot_req_pmdcurrentloopparams()
        r22 = self.mot_req_pmdsettledcurrentloopparams()
    #    r23 = self.mot_req_pmdstageaxisparams()
    
        parameters = rc,r1,r3,r4,r5,r6,r7,r8,r10,r16,r17,r18,r19,r20,r21,r22
    
        s = ''
        for parameter_set in parameters:
            s+=str(parameter_set.data)
            
        with open(filename,'w') as f:
            f.write(s)        
        
    def to_apt_pos(self,pos):
        return pos*self.enc_cnt_per_mm
    
    def to_apt_vel(self,vel):
        return vel*(self.T)*(self.enc_cnt_per_mm)

    def to_apt_acc(self,acc):
        return acc*(self.T**2)*(self.enc_cnt_per_mm)
    
    def from_apt_pos(self,pos):
        return pos/self.enc_cnt_per_mm
    
    def from_apt_vel(self,vel):
        return vel/(self.T)/(self.enc_cnt_per_mm)

    def from_apt_acc(self,acc):
        return acc/(self.T**2)/(self.enc_cnt_per_mm)

class DDS300(LinearStage):
    '''
    velocity param defaults:
    acceleration = 13744
    max_velocity = 13421773
    min_velocity = 0

    jog param defaults:
    jog_acceleration = 13744
    jog_min_velocity = 0
    jog_max_velocity = 13421773
    jog_mode = 1
    jog_step_size = 1000
    stop_mode = 2
    
    backlash_distance:  0
    relative_distance:  0
    absolute_position:  0
    '''
    
    enc_cnt_per_mm = 20000
    k_velocity = 134217.73
    k_acceleration = 13.744
    

if __name__=='__main__':
        
        
    
    controller = BBD201('73876440')
#    controller.mytype = 'ftdi'
    controller.connect()
#    
##    controller.device.write(b'\x05\x00\x00\x00\x11\x01')
##    time.sleep(.1)
##    s=controller.device.read(controller.device.inWaiting())
#    
    stage = DDS300(0x21,0x01,controller)
    stage.save_parameters()
#    
#    r_status = stage.mot_req_statusupdate()
#     
#    
    r = stage.mod_set_chanenablestate(0x01)
    r = stage.mot_move_home()
#    r = stage.mot_req_poscounter()
#    print('at position: ',stage.from_apt_pos(r.data.position.to_int()))
    data = apt_data.MOT_MOVE_RELATIVE(stage.channel,stage.to_apt_pos(10))
    r = stage.mot_move_relative(data)
    data = apt_data.MOT_MOVE_ABSOLUTE(stage.channel,stage.to_apt_pos(50))
    r = stage.mot_move_absolute(data)
##    data = apt_data.MOT_MOVE_A(stage.channel,stage.to_apt_pos(0))
##    r = stage.mot_move_jog()
#    r = stage.mot_move_velocity()
#    time.sleep(.1)
    r = stage.mot_move_stop()
    
    r = stage.mod_set_chanenablestate(0x00)
    
    controller.close()    
##
#
##data = apt_data.MOT_MOVE_ABSOLUTE(0x01,0)
###m=Message.build(md.message.MOT_MOVE_RELATIVE,dest = 0x21,data = data)
###r = controller.send_message_receive_response(m)
##r = controller.mot_move_absolute(0x21,data)
##
##received = False
##while not received:
##    r = controller.get_messages()
##    if r is not None:
##        if r.msg_id=='MOT_MOVE_COMPLETED':
##            received = True
##    time.sleep(.05)
##print(r.msg_id)
#
##r = controller.enable_channel(0x21,0x02)

#
#
##
##msg_id, data1 = r3.parse()
##d1 = apt_data.HW_GET_INFO.parse(data1)
##d1f = d1.firmware
##f = apt_types.APTLong(d1.firmware)
##print(f.to_int())