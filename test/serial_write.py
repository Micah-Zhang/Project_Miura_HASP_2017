import time 
import serial

ser = serial.Serial(
<<<<<<< HEAD
	port = '/dev/ttyUSB0',
	baudrate = 4800, # 9600, # 1200,  # 4800,  #115200,
=======
	port ='/dev/serial0',
	baudrate = 4800, #1200, #4800, #115200,
>>>>>>> 5ccceed38f8f4cf1d479c138a41a9b2f6e0d84b2
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

<<<<<<< HEAD
ser.xonxoff=1
ser.close()
ser.open()

counter = 0
while True:
	a = ser.write(b'Hello World!')
	counter += 1
	print(counter)
	time.sleep(0.5)
=======
while(True):
	x = ser.read()
	print(x)
	time.sleep(1)

#	s = ser.read(10)
#	print(s)
#	line = ser.readline()
#	print(line)
>>>>>>> 5ccceed38f8f4cf1d479c138a41a9b2f6e0d84b2
