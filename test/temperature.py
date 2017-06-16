import os
import time
import smbus
import RPi.GPIO as GPIO
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor1 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
temp_sensor2 = '//sys/bus/w1/devices/28-000007a8a632/w1_slave'
#temp_sensor3 = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'


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


for a in range(5000):
	print(1)
	print(read_temp(temp_sensor1))
	print(2)
	print(read_temp(temp_sensor2))
	time.sleep(1)
