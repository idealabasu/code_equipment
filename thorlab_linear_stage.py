import thorlabs_apt as apt

def init_thorlabs(blocking=True):
    thor_lab_address1 = apt.list_available_devices()
    #if not working using the value from thor_lab_address1
    motor = apt.Motor(94876441)    
    motor.move_home(blocking)    
    motor.set_move_home_parameters(*motor.get_move_home_parameters())
    motor.set_velocity_parameters(*motor.get_velocity_parameters())
    
    return motor



motor = init_thorlabs(blocking=True)
motor.move_home(True)

motor.set_move_home_parameters(*motor.get_move_home_parameters())
motor.set_velocity_parameters(*motor.get_velocity_parameters())


motor.set_velocity_parameters(0,1000,10)
motor.move_to(145,blocking=True)
