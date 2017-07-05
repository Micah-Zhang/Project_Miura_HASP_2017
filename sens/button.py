import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.IN)

while True:
	if (GPIO.input(32)):
		print("Button pressed")
	else:
		print("Button not pressed")
