import sched
import os
import time
import smbus
from smbus import SMBus
import RPi.GPIO as GPIO
import math
from w1thermsensor import W1ThermSensor
#import Adafruit_ADXL345
#import Adafruit_ADS1x15

# Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_buck_convertor = '//sys/bus/w1/devices/28-000007a891a3/w1_slave'
temp_motor_driver = '//sys/bus/w1/devices/28-000007a89303/w1_slave'
temp_camwall_1 = '//sys/bus/w1/devices/28-00000865ce6c/w1_slave'
temp_camwall_3 = '//sys/bus/w1/devices/28-00000865e2e7/w1_slave'
temp_camwall_2 = '//sys/bus/w1/devices/28-00000828fbdd/w1_slave'
temp_camwall_4 = '//sys/bus/w1/devices/28-000007a8af78/w1_slave'
temp_internal_ambient = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'
temp_exterior_ambient = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
temp_motor = '//sys/bus/w1/devices/28-0000086460f1/w1_slave'
GAIN = 1
bus = smbus.SMBus(1)

# Extra Setup
#accel = Adafruit_ADXL345.ADXL345()
#adc = Adafruit_ADS1x15.ADS1115()
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


# HELIOSV's temp sensor read function. I strongly prefer this over ours. 

def temp(downlink):
	#try:
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
	#except:
	#	print("Temperature reading failed")


'''
# Grab raw temp data
def temp_raw(temp_sensor):
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Process raw data and return nice data for ONE temp sensor. Will replace with HELIOSV code once verified.
def read_temp(downlink):
	try:
		lines = temp_raw(temp_sensor1)
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = temp_raw(temp_sensor1)
		temp_output = lines[1].find('t=')
		if temp_output != -1:
			temp_string = lines[1].strip()[temp_output+2:]
			temp_c = float(temp_string) /1000.0
			temp_f = temp_c * 9.0 / 5.0 + 32.0
			downlink.put(["SE", "T1", "{0:.2f}".format(temp_c)])
	except:
		pass
#		print("Temp Failed")
'''
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
#		print("Humidity Failed")

# Grab raw data from bus. Convert raw data to nice data.
def read_pres(downlink):#downlink
	try:
		data = bus.read_i2c_block_data(0x60, 0x00, 4)
		pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16 # Use with humidity sensor?
		pressure = (pres / 4.0) / 1000.0
		
		downlink.put(["SE", "PR", "{0:.2f}".format(pressure)])
#		print("sent to downlink")
#		print(["SE", "PR", "{0:.2f}".format(pressure)])
	except:
		pass
#		print("Pressure Failed")

# Grab raw data from bus. Use Adafruit library to convert to nice data.
def read_acce(downlink):
	try:
		x, y, z = accel.read()
		downlink.put(["SE", "AC", "{0:.2f}".format(x), "{0:.2f}".format(y), "{0.2f}".format(z)])
	except:
		pass
#		print("Accelerometer Failed")

# Blink LEDs with 0.5 second spacing.
def blink(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
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
