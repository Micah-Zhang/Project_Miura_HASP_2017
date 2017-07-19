import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Direction_Pin = 15
Step_Pin = 13

Upper_Button = 32
Lower_Button = 36


GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Upper_Button, GPIO.IN)
GPIO.setup(Lower_Button, GPIO.IN)

for i in range(12):
	GPIO.output(Direction_Pin, GPIO.HIGH)
	while not GPIO.input(Upper_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		time.sleep(.002)

	time.sleep(5)
	GPIO.output(Direction_Pin, GPIO.LOW)

	while not GPIO.input(Lower_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		time.sleep(.002)


