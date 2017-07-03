#most of these imports are duplicates from MOTOR.py. 
#from time import sleep
#import picamera
#import logging
#import RPi.GPIO as GPIO
#import os
#import serial
#from fmoto import minimum_success #we shouldn't have so many imports from the same file
#from fmoto import full_extension #why not just import MOTOR? it isn't very large, so there's no need to import individual functions
#from fmoto import receive_command

#tracks the cycle the payload is on
cycle = 0

#pins used for direction and step
Direction_Pin = 15
Step_Pin = 13

#set up
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarning(False)

#motor setup
#GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW) #there's no reason to duplicate setup in implementation and driver
#GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

def main():
	cycle = 1
	while cycle<3:
		fmoto.minimum_success()
		fmoto.receive_command() #why are there so many "recieve_commands"? Do we really need all of them?
		cycle+=1
	while cycle>2:
		fmoto.full_extension()
		fmoto.receive_command()
		cycle+=1

if __name__ == "__main__":
	import fmoto
	from fmoto import *
	main()
else:
	import moto.fmoto as fmoto
	from moto.fmoto import *

