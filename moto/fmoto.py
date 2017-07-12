import time
import RPi.GPIO as GPIO
import os
import serial

#need encoder stuff
Direction_Pin = 15
Step_Pin = 13

Upper_Button = 32
Lower_Button = 36

#global step = 0

#set up
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) #why is this commented out?

#motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#button setup
GPIO.setup(Upper_Button,GPIO.IN)
GPIO.setup(Lower_Button,GPIO.IN)

#move motor
def move(
	



#complete minimum success cycle
def minimum_success(moto_cmd):
	up(11160,"MS")
	print("1")
	receive_command(moto_cmd)
	print("2")
	take_4_images()
	print("3")
	ninths = 1080/9
	tempninths = ninths
	print("4")
	for opened in range(1,180):
		print("5")
		receive_command(moto_cmd)
		time.sleep(1)
		print(opened)
		if opened == ninths:
			take_4_images()
			ninths += tempninths
	down(11160, "MS")
	receive_command(moto_cmd)
	take_4_images()
	for closed in range(1,180): #what does this do?
		receive_command(moto_cmd)
		time.sleep(1)
		print(closed)

#complete full extension cycle
def full_extension(moto_cmd):
	up(15500,"FE")
	take_4_images()
	receive_command(moto_cmd)
	ninths = 1080/9
	for opened in range(1,180):
		receive_command(moto_cmd)
		print(opened)
		time.sleep(1)
		if opened == ninths:
			take_4_images()
			ninths += ninths
	down(11500, "FE")
	take_4_images()
	for closed in range(1,180):
		receive_command(moto_cmd)
		print(closed)
		time.sleep(1)

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

	while not moto_cmd.empty():
		command = moto_cmd.get_nowait()
		#nudge commands
		if command == '\xB1':
			up(200, "CM")
        		#downlink command received awknowledgement
		elif command == '\xB2':
			up(1000, "CM")
        		#downlink command received awknowledgement
		elif command == '\xB3':
			up(5000, "CM")
        		#downlink command received awknowledgement
		elif command == '\xB4':
			down(200, "CM")
       	 		#downlink command received awknowledgement
		elif command == '\xB5':
			down(1000, "CM")
        		#downlink command received awknowledgement
		elif command == '\xB6':
			down(5000, "CM")
			#downlink command received awknowledgement
		elif command == '\xB7':
			down(1, "FE")
        		#move down until button is pressed
		elif command == '\xB8':
			up(1, "FE")
        	#move up until button is pressed
		'''
		elif command == 'dwlk image':
        		#downlink image
		elif command == 'ping':
			#test for pi communication
		'''

