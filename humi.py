import smbus
import time

bus = smbus.SMBus(1) #initialization 
address = 0x40 #sensor specific
command = 0xE3 #see table below

## List of commands:
# 0xE5: Measure RH, Hold Master Mode
# 0xF5 Measure RH, No Hold Master Mode
# 0xE3: Measure Temp, Hold Master Mode
# 0xF3: Measure Temp, No Hold Master Mode
# 0xE0: Read Temperature Value from PRevious RH Measurement
# 0xFE: Reset  

#reads raw data
def raw():
	raw = bus.read_byte_data(address,command)
	return raw 

#convert raw to relative humidity
def rh(raw):
	rh = 125 * raw / 65536 - 6
	return rh

#convert raw to temperature (celsius)
def temp(raw):
	temp = 175.72 * raw / 65536 - 46.85
	return temp  
	

#continuously read and print sensor data
while True:
	data  = humi()
	print(data)
	time.sleep(1)
