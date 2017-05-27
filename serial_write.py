import time 
import serial

ser = serial.Serial(

	port = '/dev/serial0',
	baudrate = 115200,
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
	#ser.write("Write counter: {:d} \n".format(counter).encode())
	time.sleep(1)
	counter +- 1
