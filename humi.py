import smbus 
import time

bus = smbus.SMBus(1) #initialization 

## List of commands:
# 0xE5: Measure RH, Hold Master Mode
# 0xF5 Measure RH, No Hold Master Mode (DEFAULT)
# 0xE3: Measure Temp, Hold Master Mode
# 0xF3: Measure Temp, No Hold Master Mode (DEFAULT)
# 0xE0: Read Temperature Value from Previous RH Measurement
# 0xFE: Reset  

#print relative humidity (%)
def rh(hold):
	address = 0x40
	command = 0xF5
	if hold == "HM":
		command = 0xE5
	bus.write_byte(address, command) 
	time.sleep(0.3)
	data0 = bus.read_byte(address)
	data1 = bus.read_byte(address)
	rh = 125 * (data0 * 256 + data1) / 65536 - 6
	print(rh)

#print temperature (fahrenheit)
def temp(hold):
	address = 0x40
	command = 0xF3
	if hold == "HM":
		command = 0xE3
	bus.write_byte(address, command)
	time.sleep(0.3)
	data0 = bus.read_byte(address)
	data1 = bus.read_byte(address) 
	temp = 175.72 * (data0 * 256 + data1) / 65536 - 46.85
	temp = temp * 1.8 + 32
	print(temp) 
	
#continuously read and print sensor data
while True:
	setting = input("Enter 'RH' for relative humidity OR 'T' for temperature OR 'Q' to exit: ")	
	hold = input("Enter 'HM' to hold master. Else press ENTER: ")
	if setting == 'RH':
		while True:
			rh(hold)
			time.sleep(0.5)	
	elif setting == 'T':

		while True:
			temp(hold)
			time.sleep(0.5)	
	else: 
		print("quitting")
		break

#git stage -a 
