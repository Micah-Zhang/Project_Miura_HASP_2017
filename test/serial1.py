import serial
import time

port = "/dev/ttyS0"

def readLine(port):
	s = ""
	while True:
		ch = port.read()
		s += ch
		if ch == '\r':
			return s

ser = serial.Serial(port, baudrate = 1200)
print("starting")
while(True):
	time.sleep(1)
	print("sending synch")
	ser.write("A".encode())
	rcv = readLine(ser)
	print("recieved:", rcv)
	
	
