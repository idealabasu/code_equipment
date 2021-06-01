# -*- coding: utf-8 -*-
"""
Created on Mon May 31 18:20:27 2021

@author: dongting
"""

import os
import time
import socket
import numpy
import time

       

"""
Dynamixel Initialaztion

"""

# if os.name == 'nt':
#     import msvcrt
#     def getch():
# #        return msvcrt.getch().decode()
#         return msvcrt.getch()
# else:
#     import sys, tty, termios
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     def getch():
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

from dynamixel_sdk import *      

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_PRESENT_VELOCITY   = 128
ADDR_PRO_PRESENT_CURRENT   = 126
ADDR_PRO_PRPFILE_VELOCITY = 112
ADDR_PRO_OPERATING_MODE = 11
ADDR_PRO_VELOCITY_LIMIT = 44
ADDR_PRO_GOAL_VELOCITY     = 104

DXL_OPERATING_is_CURRENT = 0
DXL_OPERATING_is_VELOCITY = 1
DXL_OPERATING_is_POSITION = 3
DXL_OPERATING_is_EXTENDED_POSITION = 4
DXL_OPERATING_is_PWM = 3

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_1                     = 0             # Dynamixel ID : 1

BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
#DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
DEVICENAME                  = 'COM4'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
#DXL_MINIMUM_POSITION_VALUE  = 695           # Dynamixel will rotate between this value
#DXL_MAXIMUM_POSITION_VALUE  = 1445            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
#DXL_MOVING_STATUS_THRESHOLD = 10                # Dynamixel moving status threshold
DXL_PROFILE_SPEED = 200


DXL_PRO_GOAL_VELOCITY = 20
DXL_PRO_GOAL_CURRENT = 20


portHandler = PortHandler(DEVICENAME)

packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel_1 has been successfully connected")
    

# Position Control
dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_OPERATING_MODE,DXL_OPERATING_is_POSITION)

dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
# dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)


DXL_PROFILE_SPEED = 200
DXL_GOAL_POSITION = 1500

dxl_comm_result_1, dxl_error_1 = packetHandler.write4ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_PRPFILE_VELOCITY,DXL_PROFILE_SPEED)
dxl_comm_result_1, dxl_error_1 = packetHandler.write4ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_GOAL_POSITION, DXL_GOAL_POSITION)



# Velocity Control
# Still developing this part......
dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)

dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, ADDR_PRO_OPERATING_MODE,DXL_OPERATING_is_VELOCITY)


# # dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, 98,0)

# dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, 44, 255)

# # dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1, 112, 4720)

# dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1,104,100)

# dxl_comm_result_1, dxl_error_1 = packetHandler.write1ByteTxRx(portHandler, DXL_ID_1,65,1)
