import time 
import serial

ser = serial.Serial(
	port ='/dev/serial0',
	baudrate = 4800, #1200, #4800, #115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while(True):
	x = ser.read()
	print(x)
	time.sleep(1)

#	s = ser.read(10)
#	print(s)
#	line = ser.readline()
#	print(line)
