import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def read_humi(): #read humidity
        bus.write_byte(0x40, 0xF5)
        time.sleep(0.3)
        data0 = bus.read_byte(0x40)
        data1 = bus.read_byte(0x40)
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
        time.sleep(0.3)
        return humidity
#print(humidity)
