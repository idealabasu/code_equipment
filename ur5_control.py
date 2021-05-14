import numpy as np
import urx
import time

def Init_ur5(ur5_port):
    try:
        tcp = ((0,0,0,0,0,0))
        payload_m = 1
        payload_location = (0,0,0.5)
        global ur5
        import urx    
        ur5 = urx.Robot(ur5_port)
        ur5.set_tcp(tcp)
        ur5.set_payload(payload_m, payload_location)
        try:
            rospy.loginfo("UR5 connected")
        except:
            print("UR5 Connected")
    except:
        try:
            rospy.loginfo("Could not connect, check connection")
        except:
            print("Could not connect, check connection")


def move_ur5(moving_vector,v,a):
    current_pose = ur5.get_pose()
    current_pose.pos[:] += moving_vector
    ur5.set_pose(current_pose,vel = v,acc = a)    

def move_ur5_wait(moving_vector,v,a):
    current_pose = ur5.get_pose()
    current_pose.pos[:] += moving_vector
    ur5.set_pose(current_pose,vel = v,acc = a)    


def rotating_ur5_z(angle, v, a,flag):
    current_pose = ur5.get_pose()
    v*=0.00454319282637702
#    ur5.set_pose(current_pose,vel = v,acc = a)
    rad = rad = math.radians(angle)
    current_pose.orient.rotate_zt(rad)
#    new_pose = current_pose
    ur5.set_pose(current_pose,vel = v,acc = a,wait=flag)

ur5_port = '192.168.0.102'
vel = 1/100
acc = 1

Init_ur5()

loc=ur5.get_pose()
loc_0 = ur5.get_pos()



move_ur5(moving_vector_up*distance,vel,acc)


ur5.set_pose(loc_0,vel,acc,wait=True)
