import serial
from time import sleep

port = "/dev/ttyS0"
ser = serial.Serial(port,4800)
ser.close()
ser.open()
while(True):
	print("Sending...")
	x = ser.write("Hello".encode())
	sleep(10)
