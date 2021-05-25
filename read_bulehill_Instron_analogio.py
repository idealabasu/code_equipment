import pyfirmata
import time
import numpy
import matplotlib.pyplot as plt


#READ THE MANUAL BEFORE USE THE MACHINE

#Change the com number to your arduino
board = pyfirmata.Arduino('COM7')

it = pyfirmata.util.Iterator(board)
it.start()

x_pin = 1
y_pin = 2
y1_pin = 3
board.analog[x_pin].mode = pyfirmata.INPUT
board.analog[y_pin].mode = pyfirmata.INPUT
board.analog[y1_pin].mode = pyfirmata.INPUT

x_raw_signal = board.analog[x_pin].read()
y_raw_signal = board.analog[y_pin].read()
y1_raw_signal = board.analog[y1_pin].read()


# Attention! the raw_data s are scalled by pyfirmata. Arduino output is 0-5v and pyfirmata scalled them to 0-1. Also, you need to set the correct value on the bluehill machine so the output is inside the sensing range. READ THE MANUAL BEFORE USE THE MACHINE
