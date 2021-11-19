# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 10:22:12 2020

@author: danaukes
"""
import thorlabs_linear_stage.message_dicts as md

from thorlabs_linear_stage.apt_types import APTWord,APTDWord, APTShort, APTLong, APTByte,APTByte16,APTByte48,APTChar64,APTChar8,APTChar16

class Data(object):
    names = []
#    sizes = []
    types = []
    pass

    @classmethod
    def parse(cls,message):
        new = cls()
        ii=0
        assert(len(cls.names)==len(cls.types))
        for key, tipu in zip(cls.names,cls.types):
            length = tipu.num_bytes
            value = message[ii:(ii+length)]
            setattr(new,key+'_r',value)
            
#            if tipu is None:
#                pass
#            elif tipu == 'string':
#                setattr(new,key,value.decode())
#            else:
            setattr(new,key,tipu(value))
            ii+=length
        return new
    
    def __init__(self,*args):
        assert(len(self.names)==len(self.types))
        for key, tipu, item in zip(self.names,self.types,args):
            length = tipu.num_bytes
            
            if tipu is None:
                setattr(self,key+'_r',item)
            elif tipu == 'string':
                setattr(self,key,item)
                value = item.encode()
                l = len(value)
                if l>length:
                    setattr(self,key+'_r',value[:length])
                elif l==length:
                    setattr(self,key+'_r',value)
                else:
                    setattr(self,key+'_r',value+b'\x00'*(length-l))
            else:
                setattr(self,key,tipu.from_int(item))
                setattr(self,key+'_r',getattr(self,key).value)
                
    def __str__(self):
        string = str(type(self))+' (Data Class)'
        for item in self.names:
            string+='\n  '+item+': '+str(getattr(self,item))
        string +='\n'
        return string
    
    def __repr__(self):
        return str(self)
    
    def serialize(self):
        message = b''
        for key in self.names:
            value = getattr(self,key+'_r')
            message+=value
        return message
            

class HW_GET_INFO(Data):
    names = ['serial','model','type','firmware_minor','firmware_interim','firmware_major','firmware_unused','internal1','internal2','hw_version','mod_state','nchs']
#    sizes = [4,8,2,1,1,1,1,48,16,2,2,2]
    types = [APTLong,APTChar8,APTWord,APTByte,APTByte,APTByte,APTByte,APTByte48,APTByte16,APTWord,APTWord,APTWord]


#class MOT_GET_VELPARAMS(Data):
#    names = ['','',]
#    struct = [APTWord,]
    

class RACK_GET_BAYUSED(Data):
    names = ['bay','state']
#    sizes = [1,1]
    types = [APTByte,APTByte]


class MOT_GET_VELPARAMS(Data):
    names = ['chan_ident','min_velocity','acceleration','max_velocity']
#    sizes = [2,4,4,4]
    types = [APTWord,APTLong,APTLong,APTLong]
    
class MOT_GET_JOGPARAMS(Data):
    names = ['chan_ident','jog_mode','jog_step_size','jog_min_velocity','jog_acceleration','jog_max_velocity','stop_mode']
#    sizes = [2,2,4,4,4,4,2]
    types = [APTWord,APTWord,APTLong,APTLong,APTLong,APTLong,APTWord]
    
class MOT_GET_GENMOVEPARAMS(Data):
    names = ['chan_ident','backlash_distance']
#    sizes = [2,4]
    types = [APTWord,APTLong]

class MOT_GET_MOVERELPARAMS(Data):
    names = ['chan_ident','relative_distance']
#    sizes = [2,4]
    types = [APTWord,APTLong]

class MOT_GET_MOVEABSPARAMS(Data):
    names = ['chan_ident','absolute_position']
#    sizes = [2,4]
    types = [APTWord,APTLong]

class MOT_GET_HOMEPARAMS(Data):
    names = ['chan_ident','home_dir','limit_switch','home_velocity','offset_distance']
#    sizes = [2,2,2,4,4]
    types = [APTWord,APTWord,APTWord,APTLong,APTLong]

class MOT_MOVE_RELATIVE(Data):
    names = ['chan_ident','relative_distance']
    types = [APTWord,APTLong]

class MOT_MOVE_ABSOLUTE(Data):
    names = ['chan_ident','absolute_distance']
    types = [APTWord,APTLong]
    
class MOT_STATUS(Data):
    names = ['chan_ident','position','enc_count','status_bits']
    types = [APTWord,APTLong,APTLong,APTDWord]

class DS(Data):
    names = ['d','s']
    types = [APTByte,APTByte]
    
class MOT_MOVE_HOMED(DS):
    pass
class HW_DISCONNECT(DS):
    pass
class HW_RESPONSE(DS):
    pass

class HW_RICHRESPONSE(Data):
    names = ['msg_ident','code','notes']
    types = [APTWord,APTWord,APTChar64]
    
class MOT_GET_POSCOUNTER(Data):
    names = ['chan_ident','position']
    types = [APTWord,APTDWord]
    
class MOT_GET_POWERPARAMS(Data):    
    names = ['chan_ident','rest_factor','move_factor']
    types = [APTWord,APTWord,APTWord]

class MOT_GET_LIMSWITCHPARAMS(Data):    
    names = ['chan_ident','cw_hard_limit','ccw_hard_limit','cw_soft_limit','ccw_soft_limit','limit_mode']
    types = [APTWord,APTWord,APTWord,APTLong,APTLong,APTWord]


class MOT_MOVE_STOPPED(DS):    
    pass

class MOT_GET_BOWINDEX(Data):
    names = ['chan_ident','bow_index']
    types = [APTWord,APTWord]

class MOT_GET_DCPIDPARAMS(Data):
    names = ['chan_ident','proportional','integral','differential','integral_limit','filter_control']
    types = [APTWord,APTLong,APTLong,APTLong,APTLong,APTWord]

class MOT_GET_AVMODES(Data):
    names = ['chan_ident','mode_bits']
    types = [APTWord,APTWord]

class MOT_GET_POTPARAMS(Data):
    names = ['chan_ident','zero_wnd','vel1','wnd1','vel2','wnd2','vel3','wnd3','vel4']
    types = [APTWord,APTWord,APTLong,APTWord,APTLong,APTWord,APTLong,APTWord,APTLong]

class MOT_GET_BUTTONPARAMS(Data):
    names = ['chan_ident','mode','position1','position2','timeout','not_used']
    types = [APTWord,APTWord,APTLong,APTLong,APTWord,APTWord]

class MOT_GET_PMDPOSITIONLOOPPARAMS(Data):
    names = ['chan_ident','kp_pos','integral','i_lim_pos','differential','kd_time_pos','kout_pos','kvff_pos','kaff_pos','pos_err_lim','na1','na2']
    types = [APTWord,APTWord,APTWord,APTDWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTDWord,APTWord,APTWord]

class MOT_GET_PMDMOTOROUTPUTPARAMS(Data):
    names = ['chan_ident','cont_current_lim','energy_lim','motor_lim','motor_bias','not_used1','not_used2']
    types = [APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord]
    
class MOT_GET_PMDTRACKSETTLEPARAMS(Data):
    names = ['chan_ident','time','settle_window','track_window','not_used1','not_used2']
    types = [APTWord,APTWord,APTWord,APTWord,APTWord,APTWord]
    
class MOT_GET_PMDPROFILEMODEPARAMS(Data):
    names = ['chan_ident','mode','jerk','not_used1','not_used2']
    types = [APTWord,APTWord,APTDWord,APTWord,APTWord]

class MOT_GET_PMDJOYSTICKPARAMS(Data):
    names = ['chan_ident','js_gear_lo_max_vel','js_gear_high_max_vel','js_gear_high_low_accn','js_gear_high_high_accn','dir_sense']
    types = [APTWord,APTLong,APTLong,APTLong,APTLong,APTWord]

class MOT_GET_PMDCURRENTLOOPPARAMS(Data):
    names = ['chan_ident','phase','kp_current','ki_current','i_lim_current','i_dead_band','kff','not_used1','not_used2']
    types = [APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord]
    
class MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS(Data):
    names = ['chan_ident','phase','kp_settled','ki_settled','i_lim_settled','i_dead_band_settled','kff_settled','not_used1','not_used2']
    types = [APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord,APTWord]
    
class MOT_GET_PMDSTAGEAXISPARAMS(Data):
    names = ['stage_id','axis_id','part_no_axis','serial_num','cnts_per_unit','min_pos','max_pos','max_accn','max_dec','max_vel','res1','res2','res3','res4','res5','res6','res7','res8']
    types = [APTWord,APTWord,APTChar16,APTDWord,APTLong,APTLong,APTLong,APTLong,APTLong,APTWord,APTWord,APTWord,APTDWord,APTDWord,APTDWord,APTDWord]

class MOT_GET_STATUSUPDATE(Data):
    names = ['chan_ident','position','enc_count','status_bits']
    types = [APTWord,APTLong,APTLong,APTDWord]
    
data_types = {}
data_types['HW_GET_INFO']=HW_GET_INFO
data_types['RACK_GET_BAYUSED']=RACK_GET_BAYUSED
data_types['MOT_GET_VELPARAMS']=MOT_GET_VELPARAMS
data_types['MOT_GET_JOGPARAMS']=MOT_GET_JOGPARAMS
data_types['MOT_GET_GENMOVEPARAMS']=MOT_GET_GENMOVEPARAMS
data_types['MOT_GET_MOVERELPARAMS']=MOT_GET_MOVERELPARAMS
data_types['MOT_GET_MOVEABSPARAMS']=MOT_GET_MOVEABSPARAMS
data_types['MOT_GET_HOMEPARAMS']=MOT_GET_HOMEPARAMS
data_types['MOT_MOVE_RELATIVE']=MOT_MOVE_RELATIVE
data_types['MOT_MOVE_ABSOLUTE']=MOT_MOVE_ABSOLUTE
data_types['MOT_MOVE_COMPLETED']=MOT_STATUS
data_types['MOT_MOVE_HOMED']=MOT_MOVE_HOMED
data_types['HW_DISCONNECT']=HW_DISCONNECT
data_types['HW_RESPONSE']=HW_RESPONSE
data_types['HW_RICHRESPONSE']=HW_RICHRESPONSE
data_types['MOT_GET_POSCOUNTER']=MOT_GET_POSCOUNTER
data_types['MOT_GET_POWERPARAMS']=MOT_GET_POWERPARAMS
data_types['MOT_GET_LIMSWITCHPARAMS']=MOT_GET_LIMSWITCHPARAMS
data_types['MOT_MOVE_STOPPED']=MOT_MOVE_STOPPED
data_types['MOT_GET_BOWINDEX']=MOT_GET_BOWINDEX
data_types['MOT_GET_DCPIDPARAMS']=MOT_GET_DCPIDPARAMS
data_types['MOT_GET_AVMODES']=MOT_GET_AVMODES
data_types['MOT_GET_POTPARAMS']=MOT_GET_POTPARAMS
data_types['MOT_GET_BUTTONPARAMS']=MOT_GET_BUTTONPARAMS
data_types['MOT_GET_PMDPOSITIONLOOPPARAMS']=MOT_GET_PMDPOSITIONLOOPPARAMS
data_types['MOT_GET_PMDMOTOROUTPUTPARAMS']=MOT_GET_PMDMOTOROUTPUTPARAMS
data_types['MOT_GET_PMDTRACKSETTLEPARAMS']=MOT_GET_PMDTRACKSETTLEPARAMS
data_types['MOT_GET_PMDPROFILEMODEPARAMS']=MOT_GET_PMDPROFILEMODEPARAMS
data_types['MOT_GET_PMDJOYSTICKPARAMS']=MOT_GET_PMDJOYSTICKPARAMS
data_types['MOT_GET_PMDCURRENTLOOPPARAMS']=MOT_GET_PMDCURRENTLOOPPARAMS
data_types['MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS'] = MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS
data_types['MOT_GET_PMDSTAGEAXISPARAMS'] = MOT_GET_PMDSTAGEAXISPARAMS
data_types['MOT_GET_STATUSUPDATE']=MOT_GET_STATUSUPDATE

#data_types['MOT_GET_POTPARAMS']=MOT_GET_POTPARAMS


#data_types['MOD_SET_CHANENABLESTATE']=DS
#data_types['MOD_REQ_CHANENABLESTATE']=DS
#data_types['MOD_GET_CHANENABLESTATE']=DS

if __name__=='__main__':
    a=MOT_MOVE_RELATIVE(1,10)
