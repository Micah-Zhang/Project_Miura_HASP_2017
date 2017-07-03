import time
import RPi.GPIO as GPIO
import os
import serial

#need encoder stuff

#need button stuff

Direction_Pin = 15
Step_Pin = 13

#set up
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarning(False) #why is this commented out?

#motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#move the motor up input amount of steps
def up(steps):
	GPIO.output(Direction_Pin, GPIO.HIGH)
	quarter = steps/4
	for step in range(steps):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		time.sleep(.0036) #what does this do?
		if step == quarter: #shouldn't this be inside the for loop?
			take_4_images()
			quarter += quarter #what if "steps" is odd?

#move the motor down input amount of steps
def down(steps):
	GPIO.output(Direction_Pin, GPIO.LOW)
	quarter = steps/4
	for step in range(steps):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		time.sleep(.0036)
		if step == quarter:
			take_4_images()
			quarter += quarter

#complete minimum success cycle
def minimum_success():
	up(11160)
	receive_command()
	take_4_images()
	ninths = 1080/9
	for opened in range(1,1080):
		receive_command()
		if opened == ninths:
			take_4_images()
			ninths += ninths
	down(11160)
	receive_command()
	take_4_images()
	for closed in range(1,600): #what does this do?
		receive_command()

#complete full extension cycle
def full_extension():
	up(15500)
	take_4_images()
	receive_command()
	ninths = 1080/9
	for opened in range(1,1080):
		receive_command()
	if opened == ninths:
		take_4_images()
		ninths += ninths
	down(11500)
	take_4_images()
	for closed in range(1,600):
        	receive_command()

#take image from all four cameras and save with the current timestamp as the name
def take_4_images():
	print("Taking image") #placeholder until cameras work
	'''
	for camera in range(1,4):
        	timestamp = "{0:.2f}".format(time.time())
        	os.system('fswebcam -r 1080x720 -d /dev/video{}.format(str(camera-1)) --save {}.jpg'.format(timestamp))  
	'''

#parce through the commands
def receive_command():
	ser = serial.Serial(port='/dev/serial0',baudrate=4800,timeout=1) #1 second timeout will hold up the code. there may be a better way to do the same thing.
	command = ser.readline().decode('utf-8')
    	#nudge commands
	if command == 'move up 200':
        	up(200)
        	#downlink command received awknowledgement
	elif command == 'move up 1000':
		up(1000)
        	#downlink command received awknowledgement
	elif command == 'move up 5000':
		up(5000)
        	#downlink command received awknowledgement
	elif command == 'move down 200':
		down(200)
        	#downlink command received awknowledgement
	elif command == 'move down 1000':
		down(1000)
        	#downlink command received awknowledgement
	elif command == 'move down 5000':
		down(5000)
		#downlink command received awknowledgement
	'''
	elif command == 'move down ALW':
        	#move down until button is pressed
	elif command == 'move up ALW':
        	#move up until button is pressed
	elif command == 'dwlk image':
        	#downlink image
	elif command == 'ping':
		#test for pi communication
	'''

