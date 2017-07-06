import time
from zlib import adler32

def main(downlink):
	counter = 1
	while True:'
		label = 'CU ' + 'MI ' + 'SE '
		timestamp = "{0:.2f}".format(time.time())
		#rangefinder,ammeter = fsens.read_adc()
		#rangefinder = ' ' + "{0:.2f}".format(rangefinder)
		#ammeter = ' ' + "{0:.2f}".format(ammeter)
		#humidity = ' ' + "{0:.2f}".format(fsens.read_humi())
		#pressure = ' ' + "{0:.2f}".format(fsens.read_pres())
		#temp1 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor1))
		#accel = ' ' + "{0:.2f}".format(fsens.read_acc())
		#data = rangefinder + ammeter +  humidity + pressure + temp1 + accel
		temp1 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor1))
		temp2 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor2))
		temp3 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor3))
		temp4 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor4))
		temp5 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor5))
		temp6 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor6))
		temp7 = ' ' + "{0:.2f}".format(fsens.read_temp(temp_sensor7))
		data = temp1 + temp2 + temp3 + temp4 + temp5 + temp6 + temp7
		checksum = ' ' + str(adler32(data.encode('utf-8')) & 0xffffffff)
		packet = label + timestamp + checksum + data
		packet = packet + '\n'
                downlink.put(packet)
                name = 'test{:d}.log'.format(counter)
                fsens.save_file(name,packet)

if __name__ == '__main__':
	import fsens
	from fsens import *
	main()
else:
	import sens.fsens as fsens
	from sens.fsens import *
