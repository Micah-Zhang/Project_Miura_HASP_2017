import time 
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
pin = 35
#def blink(pin): #blink LEDs
while True:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(0.5)
	print("Led Blinking")
blink(pin)

'''
def led_on(pin): #turn on LEDs  
        GPIO.output(pin,GPIO.HIGH)

def led_off(pin): #turn off LEDs
        GPIO.output(pin,GPIO.LOW)
'''
