import time
import serial

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while True:
	x = ser.readline()
	print(x)
	with open("dwlk.txt", "a+") as f:
		f.write(str(x))
