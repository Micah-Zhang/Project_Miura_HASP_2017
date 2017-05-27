import serial
import time

port = "/dev/ttyS0"

ser = serial.Serial(port, baudrate = 1200)
print("starting")
while(True):
	time.sleep(1)
	ser.write("A")
	nbChars = ser.inWaiting()
	if nbChars > 0:
		data = ser.read(nbChars)
		print(data)

