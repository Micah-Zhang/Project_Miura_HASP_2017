import smbus 
import time

bus = smbus.SMBus(1) #initialization 
address = 0x53 #sensor specific

## List of commands:
# 0x32: X-Axis LSB (Least Significant Bit)
# 0x33  X-Axis MSB (Most Significant Bit) 
# 0x34: Y-Axis LSB
# 0x35: Y-Axis MSB
# 0x36: Z-Axis LSB
# 0x37: Z-Axis MSB  

def xaxis():
	LSB  = bus.read_byte_data(address,0x32)
	MSB = bus.read_byte_data(address,0x33)
	




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
	setting = input("Enter 'RH' for relative humidity OR 'T' for temperature OR 'Q' to exit: ")
	if setting == 'RH':
		command = 0xF5
		master = input("Enter any key for DEFAULT (no hold master). Else enter 'HM': ")
		if master == 'HM':
			command = 0xE5
			while True:
				time.sleep(1) 
				a = raw()
				b = rh(a)
				print(a,hex(int(a)),b,hex(int(b)))
		else:
			while True:
				time.sleep(1)
				a = raw()
				b = rh(a) 
				print(a,hex(int(a)),b,hex(int(b)))
	elif setting == 'T':
		command = 0xF3
		master = input("Enter any key for DEFAULT (no hold master). Else enter 'HM': ")
		if master == 'HM':
			command = 0xE3
			while True:
				time.sleep(1)
				a = raw()
				b = temp(a)
				print(a,hex(int(a)),b,hex(int(b)))
		else:
			while True:
				time.sleep(1)
				a = raw()
				b = temp(a)
				print(a,hex(int(a)),b,hex(int(b)))
	else: 
		print("quitting")
		break
	
#git stage -a 
