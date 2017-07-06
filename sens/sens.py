import time
from zlib import adler32

def main(downlink):
	counter = 1
	while True:
		downlink.put("packet")
		time.sleep(1)
		'''
		label = 'CU ' + 'MI ' + 'SE '
		timestamp = "{0:.2f}".format(time.time())
		rangefinder,ammeter = fsens.read_adc()
		rangefinder = ' ' + "{0:.2f}".format(rangefinder)
		ammeter = ' ' + "{0:.2f}".format(ammeter)
		humidity = ' ' + "{0:.2f}".format(fsens.read_humi())
		pressure = ' ' + "{0:.2f}".format(fsens.read_pres())
		temp1 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor1))
		accel = ' ' + "{0:.2f}".format(fsens.read_acc())
		data = rangefinder + ammeter +  humidity + pressure + temp1 + accel
		checksum = ' ' + str(adler32(data.encode('utf-8')) & 0xffffffff)
		packet = label + timestamp + checksum + data
		packet = packet + '\n'
		downlink.put(packet)
		name = 'test{:d}.log'.format(counter)
		fsens.save_file(name,packet)
		'''

if __name__ == '__main__':
	import fsens
	from fsens import *
	main()
else:
	import sens.fsens as fsens
	from sens.fsens import *
