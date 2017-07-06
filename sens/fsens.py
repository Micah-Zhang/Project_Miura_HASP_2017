import os
import time
import smbus
from smbus import SMBus
#import Adafruit_ADXL345
import RPi.GPIO as GPIO
#import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor1 = '//sys/bus/w1/devices/28-000007a891a3/w1_slave'
temp_sensor2 = '//sys/bus/w1/devices/28-000007a89303/w1_slave'
temp_sensor3 = '//sys/bus/w1/devices/28-000007a8a632/w1_slave'
temp_sensor4 = '//sys/bus/w1/devices/28-000007a8acab/w1_slave'
temp_sensor5 = '//sys/bus/w1/devices/28-000007a8af78/w1_slave'
temp_sensor6 = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'
temp_sensor7 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
#accel = Adafruit_ADXL345.ADXL345()
#adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
bus = smbus.SMBus(1)
#bus.write_byte_data(0x60, 0x26, 0x39) #pres

def temp_raw(temp_sensor):
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(temp_sensor): #read temperature
	lines = temp_raw(temp_sensor)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw(temp_sensor)
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) /1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f	

def read_humi(): #read humidity
	bus.write_byte(0x40, 0xF5)
	time.sleep(0.3)
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
	time.sleep(0.3)
	return humidity
'''
def read_pres():
        deg = u'\N{DEGREE SIGN}'
        ADDR = 0x60
        Ctrl_REG1 = 0x26
        PT_DATA_CFG = 0x13
        bus = SMBus(1)

        whoAmI = bus.read_byte_data(ADDR, 0x0C)
        print( hex(whoAmI))
        if whoAmI != 0xc4:
                print( "Device Not Active")
                exit(1)
        setting = bus.read_byte_data(ADDR, CTRL_REG1)
        newSetting = setting | 0x38
        bus.write_byte_data(ADDR, CTRL_REG1, newSetting)

        bus.write_byte_data(ADDR, PT_DATA_CFG, 0x07)

        setting = bus.read_byte_data(ADDR, CTRL_REG1)
        if (setting & 0x02) == 0:
                bus.write_byte_data(ADDR, CTRL_REG1, (setting | 0x02))

        print( "Waiting for data")
        status = bus.read_bytes_data(ADDR,0x00)
        time.sleep(0.5)

        print( "Reading data")
        p_data = bus.read_i2c_block_data(ADDR,0x01,3)
        t_data = bus.read_i2c_block_data(ADDR,0x04,2)
        status = bus.read_byte_data(ADDR,0x00)
        print("status:" +bin(status))

        p_msb = p_data[0]
        p_csb = p_data[1]
	p_lsb = p_data[2]
        t_msb = t_data[0]
        t_lsb = t_data[1]

        pressure = (p_msb << 10) | (p_csb << 2) | (p_lsb >> 6)
        p_decimal = ((p_lsb & 0x30) >>4) / 4.0

        print("Pressure and Temperature at "+time.strftime('%m/%d/%Y %H:%M:%S%z'))
        print( str(pressure + p_decimal))

	

'''
def read_pres(): #read pressure
	data = bus.read_i2c_block_data(0x60, 0x00, 4)
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres / 4.0) / 1000.0
	return pressure

def read_acc(): #read accelerometer
	x, y, z = accel.read()
	return x, y, z

def blink(pin): #blink LEDs
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
	return

def led_on(pin): #turn on LEDs	
	GPIO.output(pin,GPIO.HIGH)

def led_off(pin): #turn off LEDs
	GPIO.output(pin,GPIO.LOW)

def read_adc(): #read ADC
	values = [0]*4
	for i in range(4):
		values[i] = adc.read_adc(i, gain=GAIN)
	#Rangefinder conversion factor
	values[0] = 130*math.pow(values[0]/1000,-1.1)
	#Ammeter Conversion factor
	Vref = 20000
	sensitivity = 500/5000
	voltage = 4.88*(values[1])
	values[1] = (voltage - Vref) * sensitivity / 10
	return values[0], values[1]

def save_file(filename, data):
	with open(filename, "a+") as f:
		f.write(data)
