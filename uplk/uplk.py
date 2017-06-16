import time
import serial

#ser = serial.Serial(
#	port = '/dev/serial0',
#	baudrate = 4800,
#	parity = serial.PARITY_NONE,
#	stopbits = serial.STOPBITS_ONE,
#	bytesize = serial.EIGHTBITS,
#	timeout = 1
#)

def main(downlink, ser, run_exp, moto_cmd):
	while True:
		x = ser.readline().decode('utf-8')
		if len(x) > 0:
			print('received:', x)
		if x == 'start':
			run_exp.set() #start running the experiment
		elif x == 'stop motor':
			moto_cmd.put('stop')
		elif x == 'reset motor':
			moto_cmd.put('reset')
		elif x == 'nudge up':
			moto_cmd.put('nudge up')
		elif x == 'nudge down':
			moto_cmd.put('nudge down')
		elif x == 'unstuck':
			moto_cmd.put('unstuck')
		time.sleep(1)
