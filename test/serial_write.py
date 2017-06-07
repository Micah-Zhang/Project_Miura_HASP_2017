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

ser.xonxoff=1
ser.close()
ser.open()

counter = 0
while True:
	a = ser.write(b'Hello World!')
	counter += 1
	print(counter)
	time.sleep(0.5)
