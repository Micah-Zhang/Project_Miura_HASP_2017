import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

def read_adc(): #read ADC
        values = [0]*4
        for i in range(4):
                values[i] = adc.read_adc(i, gain=GAIN)
        #Rangefinder conversion factor
        values[0] = 130*math.pow(values[0]/1000,-1.1)
        #Ammeter Conversion factor
        #Vref = 20000
        #sensitivity = 500/5000
        #voltage = 4.88*(values[1])
        #values[1] = (voltage - Vref) * sensitivity / 10
        return values[0] #values[1]


