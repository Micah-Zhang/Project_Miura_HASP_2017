import time
import serial

ser = serial.Serial(
<<<<<<< HEAD
	port ='/dev/serial0',
	baudrate = 4800, #1200, #4800, #115200,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 5
)

ser.xonxoff=1

counter = 0
while(True):
=======
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 3
)

while True:
>>>>>>> 5ccceed38f8f4cf1d479c138a41a9b2f6e0d84b2
	x = ser.read()
	counter += 1
	print(x)
<<<<<<< HEAD
	print(counter)
	time.sleep(0.5)
=======
	time.sleep(1)
>>>>>>> 5ccceed38f8f4cf1d479c138a41a9b2f6e0d84b2
