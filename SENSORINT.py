import os
import time
import smbus
import adafruit_adx1345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15

#initialize temperature sensor
def temp_init():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	temp_sensor = '//sys/bus/w1/devices/28-00000829f3b5/w1_slave'
	def temp_raw():
       		f = open(temp_sensor, 'r')
        	lines = f.readlines()
        	f.close()
        	return lines
	def read_temp():
    		lines = temp_raw()
    		while lines[0].strip()[-3:] != 'YES':
        		time.sleep(0.2)
        		lines = temp_raw()
    		temp_output = lines[1].find('t=')
    		if temp_output != -1:
        		temp_string = lines[1].strip()[temp_output+2:]
        		temp_c = float(temp_string) /1000.0
        		temp_f = temp_c * 9.0 / 5.0 + 32.0
        		return temp_c, temp_f

#initialize humidity sensor
def humi_init():
	bus.write_byte(0x40, 0xF5) #relative humidity NO HOLD master mode
	time.sleep(0.3)	
	def read_humi():
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
		time.sleep(0.3)
		return humidity

#initialize pressure sensor
def pres_init():
	bus.write_byte_data(0x60, 0x26, 0x39)
	time.sleep(1)
	def read_pres():
		data = bus.read_i2c_block_data(0x60, 0x00, 4)
		pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
		pressure = (pres / 4.0) / 1000.0
		return pressure

#initialize altimeter
def alt_init():
	accel = Adafruit_ADXL345.ADXL345()
	def read_alt():
		x,y,z = accel.read()
		return x, y, z
		
#initialize LEDs
def led_init():
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)
	def blink(pin):
		GPIO.output(pin,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(pin,GPIO.LOW)
		time.sleep(1)
		return
		
#initialize ADC
def adc_init():
	adc = Adafruit_ADS1x15.ADS1115()
	GAIN = 1
		def read_ADC():
			values = [0]*4
			for i in range(4):
				values[i] = adc.read_adc(i,gain=GAIN)
			return values[1], values[2] #1 is rangefinder, 2 is ammeter

#initialize all sensors
bus = smbus.SMBus(1)
temp_init()
humi_init()
pres_init()
led_init()
adc_init()

#main
while(True):
	print(	
