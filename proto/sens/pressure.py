import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GAIN = 1
bus = smbus.SMBus(1)
#bus.write_byte_data(0x60, 0x26, 0x39) #pres

def read_pres(): #read pressure
        data = bus.read_i2c_block_data(0x60, 0x00, 4)
        pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        pressure = (pres / 4.0) / 1000.0
        return pressure
#print(pressure)
