import threading
import serial
import time 
import queue
from camera import TESTcam
from motor import TESTmotor
from sensors import TESTsensor

q = queue.Queue()

ser = serial.Serial(
	port = '/dev/tty/USB0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
ser.close()
ser.open()

def main():
	print("downlink thread verified")
	while True:
		if 'b' in locals():
			break
		else:
			a = TESTsensor.q.get()
			print("packet recieved")
			b = ser.write(bytes(a, encoding="UTF-8"))
			print("packet sent")
