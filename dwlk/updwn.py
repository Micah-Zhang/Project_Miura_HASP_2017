import time
import serial
import sys
 
ser = serial.Serial(
	port = '/dev/ttyUSB1',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

def save_file(name,x):
	with open(name,"a+") as f:
		f.write(x)
while True:
	choice = input("ENTER 'dwlk' to recieve downlink. ENTER 'uplk' to send uplk: ")
	if choice == "dwlk":
		length = input("How many times would you like to downlink?: ")
		counter = 0
		while(counter < length):
			x = ser.readline().decode("utf-8")
			print("dwlk recieved: ", x)
			save_file("dwlklog.txt",x)
			counter += 1
	else choice == "uplk":
		command = input("ENTER 'start' to start testing cycle")
		if command == "start"
			if command == "start\n":
				ser.write(bytes("start\n", encoding="UTF-8"))
				print("command sent!\n")
