import threading
import serial
import time

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

ser.close()
ser.open()

def main():
	while True:
		print("get ready")
		time.sleep(3)
		a = "First uplink command\n"		
		b = ser.write(bytes(a, encoding="UTF-8"))
		print("packet 1 sent")
		time.sleep(10)
		a = "Second uplink command\n"
		b = ser.write(byte(a, encoding="UTF-8"))
		print ("packet 2 sent")
main()
