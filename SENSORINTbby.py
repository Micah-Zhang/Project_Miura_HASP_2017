'i '    ' import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import datetime

bus = smbus.SMBus(1)

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

'''
# initialize humidity sensor
bus.write_byte(0x40, 0xF5) # relative humidity NO HOLD master mode
time.sleep(0.3)	

def read_humi():
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
	time.sleep(0.3)
	return humidity
'''

'''
# initialize pressure sensor
bus.write_byte_data(0x60, 0x26, 0x39)
time.sleep(1)
	
def read_pres():
	data = bus.read_i2c_block_data(0x60, 0x00, 4)
	pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
	pressure = (pres / 4.0) / 1000.0
	return pressure
'''

'''
# initialize accelerometer
accel = Adafruit_ADXL345.ADXL345()

def read_acc():
	x, y, z = accel.read()
	return x, y, z
'''
		
# initialize LEDs
gpio.setwarnings(False)
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
'''

# M A I N
rcount = input('ENTER desired read count: ')
f = open("test.log","w+")
for i in range(int(rcount)):
	#ranf, amm  = read_adc()
	#x, y, z = read_acc()
	ranf = 19200
	amm = 17890
	x = -5
	y = 1
	z = 10
	humi = 38.200230202
	press = 12.433343
	data = 'CU ' + 'MI ' + 'SE ' + 'checksum '  + str(datetime.datetime.now()) + ' ' + str(humi) + ' ' + str(press) + ' ' + str(ranf) + ' ' + str(amm) + ' ' + str(x) + ' ' + str(y) + ' ' + str(z) + ' ' + str(read_temp) + ' ' + str(i) 	
	print(data)
	blink(37)
	data = data + '\n'
	f.write(data)
f.close()
#print("Data Returns: CU MI Time, Temperature, Humidity, Pressure, Accelerometer")
