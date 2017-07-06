import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

pin_A = 18
pin_B = 16

GPIO.setup(pin_A, GPIO.IN)
GPIO.setup(pin_B, GPIO.IN)

counter = 0
pin_A_last_state = GPIO.input(pin_A)

while True:
	pin_A_state = GPIO.input(pin_A)
	# If states are different, that means a pulse has occured
	if pin_A_last_state != pin_A_state:
		# If the output of B is different to output of A, that means encoder is going CHANGE_ME
		if GPIO.input(pin_B) == pin_A_state: 
			counter = counter + 1
		else:
			counter = counter - 1
	print('Counter value: ', counter)
	pin_A_last_state = pin_A_state

