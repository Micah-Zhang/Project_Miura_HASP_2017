import sched
import os
import time
import smbus
import RPi.GPIO as GPIO
import math
import re
from w1thermsensor import W1ThermSensor

#LED Setup
led_pin = 35
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.setup(led_pin,False)
led_on = False

'''
temp_buck_converter = '//sys/bus/w1/devices/28-000007a891a3/w1_slave'
temp_motor_driver = '//sys/bus/w1/devices/28-000007a89303/w1_slave'
temp_camwall_1 = '//sys/bus/w1/devices/28-00000865ce6c/w1_slave'
temp_camwall_2 = '//sys/bus/w1/devices/28-00000828fbdd/w1_slave'
temp_camwall_3 = '//sys/bus/w1/devices/28-00000865e2e7/w1_slave'
temp_camwall_4 = '//sys/bus/w1/devices/28-000007a8af78/w1_slave'
temp_internal_ambient = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'
temp_exterior_ambient = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
temp_motor = '//sys/bus/w1/devices/28-0000086460f1/w1_slave'
'''

GAIN = 1
bus = smbus.SMBus(1)

# Extra Setup
bus.write_byte_data(0x60, 0x26, 0x39) #pres

#place holders. replace with actual values later
temp_max = [80.,80.,80.,80.,80.,80.,80.,80.,80.]
temp_min = [-20.,-20.,-20.,-20.,-20.,-20.,-20.,-20.,-20.]

# Handles sensor reading schedule
class PeriodicScheduler:
	def __init__(self):
		self.scheduler = sched.scheduler(time.time, time.sleep)

	def setup(self, interval, action, actionargs=()):
		self.scheduler.enter(interval, 1, self.setup, (interval, action, actionargs))
		action(*actionargs)

	def run(self):
		self.scheduler.run()


# Converts data array into string
def cs_str(data):
	out = "" # Initialize variable with empty string
	for i in range(len(data)): # Iterate through each "word" in data
		out += "{0:.2f} ".format(data[i]) # Add each word to the string "out"
	return out # Return newly formed string


def check_temp(temps):
	# Checks if any temperature readings are outisde expected values
	tempBools1 = [float(tempI) > maxI for tempI,maxI in zip(temps,temp_max)]
	tempBools2 = [float(tempII) < minII for tempII,minII in zip(temps,temp_min)]
	# Returns true if one of more things is on fire OR completely frozen. >:)
	if any(tempBools1):
		return True
	elif any(tempBools2):
		return True
	else:
		return False

 
def read_temp(downlink, temp_led):
	#try:
		data = []
		for sensor in W1ThermSensor.get_available_sensors(): # Grab temp values from all available sensors in a round robin fashion
			data.append(sensor.get_temperature())
		if check_temp(data):
			if not temp_led.is_set():
				GPIO.output(led_pin,True)
				temp_led.set()
		else:
			if temp_led.is_set():
				GPIO.output(led_pin,False)
				temp_led.clear()
		downlink.put(["SE", "T%i" % (len(data)), cs_str(data)]) # Send the packaged data packet to the downlink thread.
	#except:
	#	print("eat dick")


# Grab raw data from bus. Convert raw data to nice data.
def read_humi(downlink):
	try:
		bus.write_byte(0x40, 0xF5)
		time.sleep(0.3)
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		time.sleep(0.3)
		downlink.put(["SE", "HU", "{0:.2f}".format(humidity)])
	except:
		pass


# Grab raw data from bus. Convert raw data to nice data.
def read_pres(downlink):#downlink
	try:
		data = bus.read_i2c_block_data(0x60, 0x00, 4)
		pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16 # Use with humidity sensor?
		pressure = (pres / 4.0) / 1000.0
		downlink.put(["SE", "PR", "{0:.2f}".format(pressure)])
	except:
		pass


# Check Pi temperature, CPU usage, and disk usage
def read_hrbt(downlink):
	try:
		temp_read = os.popen("vcgencmd measure_temp").readline().replace('temp=','').replace("'C",'')
		cpu = os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip() + '%'
		disk_read = os.popen("df -h /")
		disk_read.readline()
		disk_usage = disk_read.readline() 
		disk_usage = re.findall(r'\d{1,3}%',disk_usage)[0]
		downlink.put(["SE", "HB", '{} {} {}'.format(temp_read, cpu, disk_usage).replace('\n','')])
		return
	except:
		pass
