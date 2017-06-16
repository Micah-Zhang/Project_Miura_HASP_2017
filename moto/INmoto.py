from __future__ import division
import time
import logging
import queue
import threading
import RPi.GPIO as GPIO

def main(run_exp):
	if(run_exp.is_set()):
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

        	#complete 2 cycles
        	cycle = 1
        	while cycle!=3:
                	GPIO.output(Direction_Pin, GPIO.HIGH)
                	for a in range(0, 16500):
                        	GPIO.output(Step_Pin, GPIO.HIGH)
                        	GPIO.output(Step_Pin, GPIO.LOW)
                        	time.sleep(.0036)
                	time.sleep(1080)
                	GPIO.output(Direction_Pin, GPIO.LOW)
                	for b in range(0, 16500):
                        	GPIO.output(Step_Pin, GPIO.HIGH)
                        	GPIO.output(Step_Pin, GPIO.LOW)
                       		time.sleep(.0036)
                	time.sleep(600)
                	cycle += 1
