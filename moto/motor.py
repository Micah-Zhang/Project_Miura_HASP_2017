from __future__ import division
import time
import logging
import queue
import threading
import RPi.GPIO as GPIO

def main():
	Direction_Pin = 15
	Step_Pin = 13
	Sleep_Pin = 11
	M0 = 29
	M1 = 31
	Micro = 1/16

	print("motor thread initialzied")

	#file to hold how far the motor has moved
	Motor_Status_File = "/home/pi/miura/motor_status.txt"


	#initialize the motor

	GPIO.setmode(GPIO.BOARD)

	#GPIO.setup(Sleep_Pin, GPIO.OUT)
	#GPIO.output(Sleep_Pin, True)

	GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

	#GPIO.setup(M0, GPIO.OUT, initial=GPIO.HIGH)
	#GPIO.setup(M1, GPIO.OUT, initial=GPIO.HIGH)
	'''
	#ask for user input
	direction = input("Would you like to move up or down, please enter up or down")
	#tell motor to move either up or down
	#UP = GPIO.HIGH, Down = GPIO.LOW
	if direction == "up":
		GPIO.output(Direction_Pin, GPIO.HIGH)
	elif direction == "down":
		GPIO.output(Direction_Pin, GPIO.LOW)
	else:
		print("enter up or down please")
	#tell motor to move XX number of steps
	#ask for user input
	steps = int(input("How many steps would you like to move?"))
	for i in range(0, steps):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		time.sleep(.002) #delay
	'''
	#complete 3 cycles
	cycle = 1
	height = 11550
	while cycle!=7:
		GPIO.output(Direction_Pin, GPIO.HIGH)
		for a in range(0, height):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			time.sleep(.0036)
		time.sleep(1080)
		GPIO.output(Direction_Pin, GPIO.LOW)
		for b in range(0, height):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			time.sleep(.0036)
		time.sleep(600)
		cycle += 1
		if cycle == 3:
			height = 16500
	
