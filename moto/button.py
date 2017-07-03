import RPi.GPIO as GPIO
import time
import os

buttonPin = 17
prev_input = 0
GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonPin,GPIO.IN)
input = GPIO.input(17)

while True:
#	if (GPIO.input(buttonPin)):
#		os.system("python3 /home/pi/miura/sens/....py")		

#	input = GPIO.input(17)
#	if ((not prev_input) and input):
#		print("Button Pressed...")
#	prev_input = input
#	time.sleep(0.05)
	if GPIO.input(17):
		print("Button Not Pressed")
		time.sleep(1)
