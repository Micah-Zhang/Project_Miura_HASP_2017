import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#temp_sensor1 = '//sys/bus/w1/devices/28-000007a8d22b/w1_slave'
#temp_sensor2 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'
#temp_sensor5 = '//sys/bus/w1/devices/28-000007a88d61/w1_slave'
#temp_sensor3 = '//sys/bus/w1/devices/28-000007a8b7a1/w1_slave'
#temp_sensor4 = '//sys/bus/w1/devices/28-000007a8a632/w1_slave'
temp_sensor2 = '//sys/bus/w1/devices/28-000007a8c380/w1_slave'

def temp_raw(temp_sensor2):
        f = open(temp_sensor2, 'r')
        lines = f.readlines()
        f.close()
        print(lines)
        return lines
def read_temp(temp_sensor2): #read temperature
        lines = temp_raw(temp_sensor2)
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = temp_raw(temp_sensor2)
        temp_output = lines[1].find('t=')
        if temp_output != -1:
                temp_string = lines[1].strip()[temp_output+2:]
                temp_c = float(temp_string) /1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                print(temp_string)
                print(temp_f)
                return temp_f

