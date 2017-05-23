import time
from w1thermsensor import W1ThermSensor

def temp(downlink,tempLED):
	try:
		data_raw = []
		data = []
		for sensor in W!ThermSensor.get_avaliable_sensors():
			data_raw.append(sensor.get_temperature())
		for i in range(len(data_raw)):
			data.append(data_raw[i])
		if (not tempLED.is_set()) and tempCheck(data):
			tempLED.set()
		downlink.put(["SE","T%i" % (len(data)), cs_str(data)])
	except:
		print("Temperature reading failed")

