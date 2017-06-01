import time
import serial

ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 9600,
	parity = serial.PARITY_ODD,
	stopbits = serial.STOPBITS_TWO,
	bytesize = serial.SEVENBITS
)

ser.isOpen()

print("Enter your command below.\r\nInsert 'exit' to leave the application.")

input = 1
while(True):
	# get keyboard input
	input = input()
	if(input == "exit"):
		ser.close()
		exit()
	else:
		# send the character to the device
		ser.write(input + '\r\n')
		out = ""
		time.sleep(1)
		while(ser.inWaiting() > 0):
			out += ser.read(1)
		
		if(out != ""):
			print(">>" + out)
			
