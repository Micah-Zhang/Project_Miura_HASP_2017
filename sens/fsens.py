import sched
import os
import time
import smbus
import RPi.GPIO as GPIO
import math
import re
from w1thermsensor import W1ThermSensor

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

'''
temp_sensor1 = '//sys/bus/w1/devices/28-000007a891a3/w1_slave'
temp_sensor2 = '//sys/bus/w1/devices/28-000007a89303/w1_slave'
temp_sensor3 = '//sys/bus/w1/devices/28-000007a8a632/w1_slave'
temp_sensor4 = '//sys/bus/w1/devices/28-000007a8acab/w1_slave'
temp_sensor5 = '//sys/bus/w1/devices/28-000007a8af78/w1_slave'
temp_sensor6 = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'
temp_sensor7 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
'''

GAIN = 1
bus = smbus.SMBus(1)

# Extra Setup
bus.write_byte_data(0x60, 0x26, 0x39) #pres


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
		out += "%f " % (data[i]) # Add each word to the string "out"
	# out += "%f" % (data[-1])
	return out # Return newly formed string

 
def read_temp(downlink):
	try:
		data_raw = []
		data = []
		for sensor in W1ThermSensor.get_available_sensors(): # Grab temp values from all available sensors in a round robin fashion
			data_raw.append(sensor.get_temperature())
		for i in range(len(data_raw)): # Copy raw temp values into file meant for converted values. Was not fully implemented.
			data.append(data_raw[i])
			#data.append(temp_cal[i] + data_raw[i])
		#if (not tempLED.is_set()) and tempCheck(data): # If any temp sensors are overheating and the temp LED is not on, turn it on.
			# If the flag isn't set, and things are on fire.
			#tempLED.set()
		downlink.put(["SE", "T%i" % (len(data)), cs_str(data)]) # Send the packaged data packet to the downlink thread.
	except:
		pass


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


# Blink LEDs with 0.5 second spacing.
def blink(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
	return


# Check Pi temperature, CPU usage, and disk usage
def read_hrbt(downlink):
	temp_read = os.popen("vcgencmd measure_temp").readline().replace('temp=','').replace("'C",'')
	cpu = os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip() + '%'
	disk_read = os.popen("df -h /")
	disk_read.readline()
	disk_usage = disk_read.readline() 
	disk_usage = re.findall(r'\d{1,3}%',disk_usage)[0]
	downlink.put(["SE", "HB", '{} {} {}'.format(temp_read, cpu, disk_usage).replace('\n','')])
	return


# Turn LEDs on
def led_on(pin):
	GPIO.output(pin,GPIO.HIGH)

# Turn off LEDs
def led_off(pin):
	GPIO.output(pin,GPIO.LOW)

# Save file
def save_file(filename, data):
	with open(filename, "a+") as f:
		f.write(data)


