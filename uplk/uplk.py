import time
import serial
import sys
sys.path.append('/home/pi/miura')
import func
from func import *

ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

def main():
	while True:
		while True:
			x = ser.readline().decode("utf-8")
			if x == "First uplink command\n":
				print("First uplink command recieved!")
				func.save_file("uplk.log",x)
				break
		x = ser.readline().decode("utf-8")
		if x == "Second uplink command\n":
			print("Second uplink command recieved!")
			func.save_file("uplk.log",x)
			break
main()
