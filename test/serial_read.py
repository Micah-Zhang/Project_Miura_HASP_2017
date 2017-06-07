import time 
import serial

ser = serial.Serial(
	port ='/dev/serial0',
	baudrate = 4800, #1200, #4800, #115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 5
)

ser.xonxoff=1

counter = 0
while(True):
	x = ser.read()
	counter += 1
	print(x)
	print(counter)
	time.sleep(0.5)
