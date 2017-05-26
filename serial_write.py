import time 
import serial

ser = serial.Serial(

	port = '/dev/ttyS0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1

)

#time.sleep(5)

counter = 0

while(True):
	print("sending...")
	ser.write("1".encode())
	time.sleep(1)
