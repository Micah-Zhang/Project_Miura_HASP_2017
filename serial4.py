import serial
from time import sleep

port = "/dev/ttyUSB0"
ser = serial.Serial(port, 4800, timeout = 0)

while(True):
	data = ser.read(9999)
	if (len(data) > 0):
		print("Got:",data)

	sleep(0.5)
	print("Not blocked")

ser.close()
