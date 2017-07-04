import time
import serial

ser = serial.Serial(
	port = '/dev/serial0',
	baudrate = 4800,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1
)

def main(downlink, run_exp, moto_cmd):
	while True:
		cmd = ser.readline().decode('utf-8')
		if cmd == 'start':
			run_exp.set() #start running the experiment
		elif cmd == 'move up 200':
			moto_cmd.put('move up 200') #nudge commands
		elif cmd == 'mvoe up 1000':
			moto_cmd.put('move up 1000')
		elif cmd == 'move up 5000':
			moto_cmd.put('move up 5000')
		elif cmd == 'move down 200':
			moto_cmd.put('move down 200')
		elif cmd == 'move down 1000':
			moto_cmd.put('move down 1000')
		elif cmd == 'move down 5000':
			moto_cmd.put('move down 5000')
		time.sleep(1) #conserve system resources
