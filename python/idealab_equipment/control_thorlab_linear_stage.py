"""
configuring this device is a little bit tricky
Please refer to: https://github.com/qpit/thorlabs_apt to install the library and copy the .dll fils
"""

import thorlabs_apt as apt

def init_thorlabs(blocking=True):
    thor_lab_address1 = apt.list_available_devices()
    #if not working using the value from thor_lab_address1
    motor = apt.Motor(94876441)    
    motor.move_home(blocking)    
    motor.set_move_home_parameters(*motor.get_move_home_parameters())
    motor.set_velocity_parameters(*motor.get_velocity_parameters())
    
    return motor

# Here we initialize the device and move the linear stage to its home position
motor = init_thorlabs(blocking=True)
motor.move_home(True)

# Here is to initialize the parameters
motor.set_move_home_parameters(*motor.get_move_home_parameters())
motor.set_velocity_parameters(*motor.get_velocity_parameters())

# Here we set the min_vel, acc and max_vel of the linear stage
# Then we move the linear stage to 145mm
motor.set_velocity_parameters(0,1000,10)
motor.move_to(145,blocking=False)

# Here  we move the linear stage by 10mm
motor.set_velocity_parameters(0,1000,10)
motor.move_by(10,blocking=False)
