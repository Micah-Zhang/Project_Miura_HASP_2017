import time 
import serial

ser = serial.Serial(

	port = '/dev/ttyUSB0',
	baudrate = 4800, # 9600, # 1200,  # 4800,  #115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)
ser.close()
ser.open()
while(True):
	print(ser.name)
	a = ser.write(b'Hello World!')
	print(a)
	time.sleep(1)
