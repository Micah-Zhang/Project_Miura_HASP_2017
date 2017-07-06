import RPi.GPIO as GPIO
import time

A_Channel = 38
B_Channel = 40
Ticks = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(A_Channel, GPIO.IN)
GPIO.setup(B_Channel, GPIO.IN)

while True:
	time.sleep(1)
	print()
	print(str(GPIO.input(38))+' '+str(GPIO.input(40)))
