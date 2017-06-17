import time
from zlib import adler32
#import sens.sensors as sensors
from sens import sensors
from sens.sensors import *

'''
if __name__ == '__main__':
	import sensors
	main()
else:
	import sens.sensors as sensors
	from sens.sensors import *
'''

def main(downlink):
	counter = 1
	while True:
		label = 'CU ' + 'MI ' + 'SE '
		timestamp = "{0:.2f}".format(time.time())
		rangefinder,ammeter = sensors.read_adc()
		rangefinder = ' ' + "{0:.2f}".format(rangefinder)
		ammeter = ' ' + "{0:.2f}".format(ammeter)
		humidity = ' ' + "{0:.2f}".format(sensors.read_humi())
		#pressure = ' ' + "{0:.2f}".format(sensors.read_pres())
		#temp1 = ' ' + "{0:.2f}".format(sensors.read_temp(temp_sensor1))
		temp = ' ' + "{0:.2f}".format(sensors.read_temp(temp_sensor))
		#temp3 = ' ' + "{0:.2f}".format(sensors.read_temp(temp_sensor3))
		temp4 = ' ' + "{0:.2f}".format(sensors.read_temp(temp_sensor4))
		#accel = ' ' + "{0:.2f}".format(sensors.read_acc())
		#data = humidity + temp + rangefinder + ammeter
		data = rangefinder + ammeter +  humidity +  temp + temp4
		#data = humidity + pressure + temp
		#data = temp2
		#data = "junk"
		checksum = ' ' + str(adler32(data.encode('utf-8')) & 0xffffffff)
		packet = label + timestamp + checksum + data
		packet = packet + '\n'
		downlink.put(packet)
		#print(packet)
		name = 'test{:d}.log'.format(counter)
		sensors.save_file(name,packet)

#if __name__ == '__main__':
#        import sensors
#        main()
#else:
#        import sens.sensors as sensors
#        from sens.sensors import *

#main()
