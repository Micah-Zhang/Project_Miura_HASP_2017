import datetime
import time
from zlib import adler32
import queue
import sys
sys.path.append('/home/pi/miura')
from dwlk import dwlk
import func
from func import *

q = queue.Queue()

def main():
	counter = 1
	while True:
		cmd = q.get
		if cmd == "sens\n":
			dwlk.q.put("uplk recieved (sens)\n")
		label = 'CU ' + 'MI ' + 'SE '
		timestamp = "{0:.2f}".format(time.time())
		#rangefinder,ammeter = func.read_adc()
		#rangefinder = ' ' + "{0:.2f}".format(rangefinder)
		#ammeter = ' ' + "{0:.2f}".format(ammeter)
		#humidity = ' ' + "{0:.2f}".format(func.read_humi())
#		pressure = ' ' + "{0:.2f}".format(func.read_pres())
		#temp1 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor1))
		#temp = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor))
		#temp3 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor3))
#		temp4 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor4))
#		accel = ' ' + "{0:.2f}".format(func.read_acc())
		
		#data = humidity + temp + rangefinder + ammeter
		#data = rangefinder + humidity + pressure + temp + accel
		#data = humidity + pressure + temp
		#data = temp2
		#data = "junk"
		checksum = ' ' + str(adler32(data.encode('utf-8')) & 0xffffffff)
		packet = label + timestamp + checksum + data
		print(packet)
		packet = packet + '\n'
		dwlk.q.put(packet)
		name = 'test{:d}.log'.format(counter)
		func.save_file(name,packet)

main()
