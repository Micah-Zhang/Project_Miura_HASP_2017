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
GPIO.setwarnings(False) #why is this commented out?

#motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#button setup
GPIO.setup(32,GPIO.IN)
GPIO.setup(36,GPIO.IN)

#move the motor up input amount of steps
def up(steps,cycle_type):
	GPIO.output(Direction_Pin, GPIO.HIGH)
	quarter = steps/4
	if (cycle_type == "MS" or cycle_type == "CM"):
		for step in range(steps):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			time.sleep(.0036) #what does this do?
			if step == quarter: #shouldn't this be inside the for loop?
				take_4_images()
				quarter += quarter #what if "steps" is odd?
	else:
		while not (GPIO.input(32)):
			GPIO.output(Step_Pin, GPIO.HIGH)
			GPIO.output(Step_Pin, GPIO.LOW)
			step += 1
			time.sleep(.0036)
			if step == quarter:
				take_4_images()
				quarter += quarter

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
def minimum_success(moto_cmd):
	up(11160,"MS")
	receive_command(moto_cmd)
	take_4_images()
	ninths = 1080/9
	for opened in range(1,1080):
		receive_command(moto_cmd)
		if opened == ninths:
			take_4_images()
			ninths += ninths
	down(11160)
	receive_command(moto_cmd)
	take_4_images()
	for closed in range(1,600): #what does this do?
		receive_command(moto_cmd)

#complete full extension cycle
def full_extension(moto_cmd):
	up(15500,"FE")
	take_4_images()
	receive_command(moto_cmd)
	ninths = 1080/9
	for opened in range(1,1080):
		receive_command(moto_cmd)
	if opened == ninths:
		take_4_images()
		ninths += ninths
	down(11500)
	take_4_images()
	for closed in range(1,600):
        	receive_command(moto_cmd)

#take image from all four cameras and save with the current timestamp as the name
def take_4_images():
	print("Taking image") #placeholder until cameras work
	'''
	for camera in range(1,4):
        	timestamp = "{0:.2f}".format(time.time())
        	os.system('fswebcam -r 1080x720 -d /dev/video{}.format(str(camera-1)) --save {}.jpg'.format(timestamp))  
	'''

#parce through the commands
def receive_command(moto_cmd):
	#ser = serial.Serial(port='/dev/serial0',baudrate=4800,timeout=1) #1 second timeout will hold up the code. there may be a better way to do the same thing.
	#command = ser.readline().decode('utf-8')
	command = moto_cmd.get()
	#nudge commands
	if command == 'move up 200':
		up(200, "CM")
        	#downlink command received awknowledgement
	elif command == 'move up 1000':
		up(1000, "CM")
        	#downlink command received awknowledgement
	elif command == 'move up 5000':
		up(5000, "CM")
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
	elif command == 'move down ALW':
		down(1)
        	#move down until button is pressed
	elif command == 'move up ALW':
		up(1, "FE")
        	#move up until button is pressed
	'''
	elif command == 'dwlk image':
        	#downlink image
	elif command == 'ping':
		#test for pi communication
	'''

