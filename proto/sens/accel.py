import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#accel = Adafruit_ADXL345.ADXL345()
adc = Adafruit_ADS1x15.ADS1115()

def read_acc(): #read accelerometer
        x, y, z = accel.read()
        return x, y, z

