import numpy as np
import urx
import time

import numpy as np

def Init_ur5(ur5_port):
    try:
        tcp = ((0,0,0,0,0,0))
        payload_m = 1
        payload_location = (0,0,0.5)
        import urx      
        ur5 = urx.Robot(ur5_port)
        ur5.set_tcp(tcp)
        ur5.set_payload(payload_m, payload_location)
    except:
            print("Can not connect, check connection and try again")    
    if ur5 == None:
        print("Can not connect, check connection and try again")
    elif ur5.host == ur5_port:
        print("UR5 connected at: " + ur5_port)
    else:
        print("Can not connect, check connection and try again")    
    return ur5
    

def move_ur5(ur5,moving_vector,v,a,wait=False):
    current_pose = ur5.get_pose()
    current_pose.pos[:] += moving_vector
    ur5.movel(current_pose,vel=v,acc=a,wait=wait)

def rotating_ur5_z(ur5,angle, v, a,wait=False):
    #in degreee
    import math
    current_pose = ur5.get_pose()
    v*=0.00454319282637702
    rad  = math.radians(angle)
    current_pose.orient.rotate_zt(rad)
    ur5.set_pose(current_pose,vel = v,acc = a,wait=wait)
  
# for ur5e
moving_vector_left = np.array((0.001,0,0))
moving_vector_right = np.array((-0.001,0,0))
moving_vector_forward = np.array((0,-0.001,0))
moving_vector_backward = np.array((0,0.001,0))
moving_vector_up = np.array((0,0,0.001))
moving_vector_down = np.array((0,0,-0.001))

#for ur5-cb
moving_vector_left = np.array((0.001,0.001,0))*math.sqrt(2)/2
moving_vector_right = -np.array((0.001,0.001,0))*math.sqrt(2)/2
moving_vector_forward = np.array((0.001,-0.001,0))*math.sqrt(2)/2
moving_vector_backward = np.array((-0.001,0.001,0))*math.sqrt(2)/2
moving_vector_up = np.array((0,0,0.001))
moving_vector_down = np.array((0,0,-0.001))


ur5e = Init_ur5("192.168.1.103")

#ur5cb = Init_ur5("192.168.1.104")


loc=ur5e.get_pose()

move_ur5(ur5e,moving_vector_up,0.01,1,wait=False)
rotating_ur5_z(ur5e,10,1,wait=False)
