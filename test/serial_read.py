import time
import serial

ser = serial.Serial(
	port = '/dev/ttyserial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

while True:
	x = ser.read()
	print(x)
	time.sleep(1)
