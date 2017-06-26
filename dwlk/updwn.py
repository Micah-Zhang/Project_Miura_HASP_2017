import time
import serial

ser = serial.Serial()
ser.baud = 4800
ser.port = '/dev/ttyUSB0'
ser.timeout = 3
ser.open()
#ser.write(b'hello')
#ser.write('hello'.encode('utf-8'))
#ser.readline()
#ser.readline().decode('utf-8')

''' 
ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 4800,
#	parity = serial.PARITY_NONE,
#	stopbits = serial.STOPBITS_ONE,
#	bytesize = serial.EIGHTBITS,
	timeout = 1
)


ser.close()
ser.open()
ser.write(b'test')
#ser.write("hello\n".encode('utf-8'))

#	x = ser.readline().decode('utf-8')
#	print(x)

def save_file(name,x):
	with open(name,"a+") as f:
		f.write(x)

while True:
	choice = input("ENTER 'dwlk' to recieve downlink. ENTER 'uplk' to send uplk: ")
	if(choice == "dwlk"):
		length = input("How many times would you like to recieve downlink?: ")
		counter = 0
		while(counter < int(length)):
			x = ser.readline().decode('utf-8')
			print(x)
			save_file("dwlklog.txt",x)
			counter += 1
	elif(choice == "uplk"):
		command = input("ENTER 'start' to start testing cycle: ")
		if command == "start":
			ser.write(bytes("start\n", encoding="UTF-8"))
			print("command sent!")
'''
