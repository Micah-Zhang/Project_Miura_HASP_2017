import time
import serial

ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

ser.close()
ser.open()

while True:
	packet = ser.readline().decode("utf-8")
	print(packet)
	with open("/home/micah/dwlk.log", "a+") as log:
		log.write(packet)
