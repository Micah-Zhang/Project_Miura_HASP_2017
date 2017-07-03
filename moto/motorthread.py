from time import sleep
import picamera
import logging
import RPi.GPIO as GPIO
import os
import serial
from MOTOR import minimum_success
from MOTOR import full_extension
from MOTOR import receive_command

#tracks the cycle the payload is on
cycle = 0

#pins used for direction and step
Direction_Pin = 15
Step_Pin = 13

#set up
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarning(False)

#motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

def main():
	cycle = 1
	while cycle<3:
		minimum_success()
		receive_command()
		cycle+= 1
	while cycle>2:
		full_extension()
		receive_command()
		cycle+=1

if __name__ == "__main__":
	main()        
                        
                        
                
                











                
