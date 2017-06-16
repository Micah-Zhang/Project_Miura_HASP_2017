import time
import serial
import sys
 
ser = serial.Serial(
	port = '/dev/serial0',
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
	if(choice == "dwlk"):
		length = input("How many times would you like to recieve downlink?: ")
		counter = 0
		while(counter < int(length)):
			x = ser.readline().decode('utf-8')
			print(x)
			#print("dwlk recieved: ", x)
			save_file("dwlklog.txt",x)
			counter += 1
	elif(choice == "uplk"):
		command = input("ENTER 'start' to start testing cycle: ")
		if command == "start":
			ser.write(bytes("start\n", encoding="UTF-8"))
			print("command sent!")
