import threading
import serial
import time
import queue
import sys
sys.path.append('/home/pi/miura')
import func
from func import *

q = queue.Queue()

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

ser.close()
ser.open()
def main():
	counter = 0
	while True:
#		a = q.get()		
		a = "hi micah\n"
		#b = ser.write(bytes(a,'utf-8'))
		ser.write(a.encode('utf-8'))
		print("packet sent",counter)
		time.sleep(1)
		counter+=1
main()
