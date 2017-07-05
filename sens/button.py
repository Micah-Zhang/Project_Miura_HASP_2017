import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.IN)
GPIO.setup(36,GPIO.IN)
while True:
	time.sleep(1)
	if (GPIO.input(32)):
		print("Button 1 pressed")
	
	if (GPIO.input(36)):
		print("Button 2 pressed")
