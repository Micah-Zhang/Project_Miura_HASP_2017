import os
import time
import smbus
import Adafruit_ADXL345
import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

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

