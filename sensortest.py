import smbus
import time
bus = smbus.SMBus(1)
address = 0x40

def humi():
	humi = bus.read_byte_data(address,0)
	return humi 

while True:
	data  = humi() #this returns the value to 1 decimal place in deg 
	print(data)
	time.sleep(1)
