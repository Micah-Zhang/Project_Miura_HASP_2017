import datetime
import time
from zlib import adler32
import sys
sys.path.append('/home/pi/miura')
from dwlk import dwlk
import func
from func import *

def main():
	counter = 1
	while True:
		label = 'CU ' + 'MI ' + 'SE '
		timestamp = "{0:.2f}".format(time.time())
		rangefinder, ammeter = func.read_adc()
		rangefinder = ' ' + "{0:.2f}".format(rangefinder)
		ammeter = ' ' + "{0:.2f}".format(ammeter)
		humidity = ' ' + "{0:.2f}".format(func.read_humi())
		temp1 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor1))
		temp2 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor2))
		temp3 = ' ' + "{0:.2f}".format(func.read_temp(temp_sensor3))
		data = rangefinder + ammeter + humidity + temp1 + temp2 + temp3
		checksum = ' ' + str(adler32(data.encode('utf-8')) & 0xffffffff)
		packet = label + timestamp + checksum + data
		print(packet)
		packet = packet + '\n'
		dwlk.q.put(packet)
		name = 'test{:d}.log'.format(counter)
		func.save_file(name,packet)
