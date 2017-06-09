import threading
import serial
import time

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
	while True:
		a = "start\n"
		ser.write(bytes(a, encoding="UTF-8"))
main()
