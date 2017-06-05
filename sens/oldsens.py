#ALEX OR MICAH! I COULDN'T FIGURE OUT HOW TO MAKE THE HUMIDITY STOP READING THOSE FAKE VALUES, THE CODE FOR THE HUMIDITY SENSOR WILL GIVE YOU REAL 
import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import datetime
from zlib import adler32
import queue

GPIO.setwarnings(False)
bus = smbus.SMBus(1)
q = queue.Queue()
print("sensor thread initialzed")

# initialize temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '//sys/bus/w1/devices/28-00000829f3b5/w1_slave'

def temp_raw():
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	time.sleep(1)
	lines = temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw()
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) /1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f

# initialize humidity sensor
bus = smbus.SMBus(1)

bus.write_byte(0x40, 0xF5) # relative humidity NO HOLD master mode
time.sleep(0.3)	

def read_humi():
	#bus.write_byte(0x40, 0xF5)
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
	time.sleep(0.3)
	return humidity#, data0, data1
'''
#NOT HOOKED UP YET!!!!
# initialize pressure sensor
bus.write_byte_data(0x60, 0x26, 0x39)
time.sleep(1)
	
def read_pres():
	data = bus.read_i2c_block_data(0x60, 0x00, 4)
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres / 4.0) / 1000.0
	return pressure
#NOT HOOKED UP YET!!!
# initialize accelerometer
accel = Adafruit_ADXL345.ADXL345()

def read_acc():
	x, y, z = accel.read()
	return x, y, z

# initialize LEDs
GPIO.setmode(GPIO.BOARD)

def blink(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
	return

def led_on(pin):
	GPIO.output(pin,GPIO.HIGH)

def led_off(pin):
	GPIO.output(pin,GPIO.LOW)
'''		
# initialize ADC
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

def read_adc():
	values = [0]*4
	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)
	return values[0], values[1]

# M A I N

def main():
	print("motor thread initialized")
	while True:
		with open("test.log", "a") as f:
			f.write(data3)
		#f = open("test.log","w+")
		ranf, amm  = read_adc()
		#x, y, z = read_acc()
		data1 = 'CU ' + 'MI ' + 'SE '
		date = str(time.time())
		#data2 = str("humi" + ' ' + "press"  + ' ' + str(ranf) + ' ' + str(amm) + ' ' + "acc x" + ' ' + "acc y" + ' ' + "acc z" + ' ' + str(read_temp()))
		data2 = str('RF: ' + str(ranf) + ' AM: ' +  str(amm) + ' HU: ' + str(read_humi()))
		data22 = data2.encode('utf-8')
		data12 = data1.encode('utf-8')
		checksum = adler32(data12+data22) & 0xffffffff
		check = str(checksum)
		check = ' '
		print(data1,date,checksum,data2)
		data2 = data2 + '\n'
		data3 = str(data1) + str(date) + str(checksum) + str(data2)
		#f.write(data3)
		#f.close()
		#blink(37)
		q.put(data3)

