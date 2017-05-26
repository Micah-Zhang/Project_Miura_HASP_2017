import time 
import serial

ser = serial.Serial(

	port ='/dev/ttyUSB0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1

)

counter = 0

while(True):
	print("reading...")
	x = ser.read()
	print(x)
