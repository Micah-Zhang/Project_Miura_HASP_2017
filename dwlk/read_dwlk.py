import time
import serial
import sys
sys.path.append('/home/pi/miura')
import func
from func import *
 
ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while True:
	x = ser.readline().decode("utf-8")
	print(x)
	func.save_file("dwlk.log", x)

