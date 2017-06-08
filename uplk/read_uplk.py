import time
import serial

ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while True:
	x = ser.readline().decode("utf-8")
	if x == "Hello Lucas!\n":
		print("Hi there!")
		with open("uplk.txt", "a+") as f:
			f.write(str(x))
		break
