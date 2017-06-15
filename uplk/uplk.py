import time
import serial
import sys
sys.path.append('/home/pi/miura')
from dwlk import dwlk
import func
from func import *

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

def main():
	while True:
		x = ser.readline().decode("utf-8")
		if x == "start\n":
			print("YES!!!")
			dwlk.q.put("start command recieved!\n")
		time.sleep(1)
