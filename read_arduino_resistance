import pyfirmata
import time
import numpy
import matplotlib.pyplot as plt


board = pyfirmata.Arduino('COM7')

it = pyfirmata.util.Iterator(board)
it.start()

res_pin = 1
board.analog[res_pin].mode = pyfirmata.INPUT

def read_res(board,res_pin):
    raw_signal = board.analog[res_pin].read()
    vout = raw_signal*5+1e-8
    vin =  5
    r1 = 22e3
    r2 = (vin/vout - 1)*r1
    return r2
  
while True:
  print(r2)
