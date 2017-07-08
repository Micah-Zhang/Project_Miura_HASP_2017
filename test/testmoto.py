import time
import RPi.GPIO as GPIO

Direction_Pin = 15
Step_Pin = 13

Upper_Button = 32
Lower_Button = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Upper_Button, GPIO.IN)
GPIO.setup(Lower_Button, GPIO.IN)

direction = ""
while not (direction == "up" or direction == "down"):
	direction = input("Please enter up or down")
	if (direction == "up"):
		GPIO.output(Direction_Pin, GPIO.HIGH)
		while not (GPIO.input(Upper_Button)):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			time.sleep(.0036)
	elif (direction == "down"):
		GPIO.output(Direction_Pin, GPIO.LOW)
		while not (GPIO.input(Lower_Button)):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			time.sleep(.0036)
