from time import sleep
import picamera
import logging
import RPi.GPIO as GPIO
import os

#tracks the cycle the payload is on
cycle = 0
#is_stuck is false when the motor is not stuck, true when it is stuck
is_stuck = False
#High_Resolution is false when a 720p resolution picture is wanted, true when a higher resolution images is wanted
High_Resolution = False
#terminate is always false until a command is sent to terminate the entire thread
terminate = False
#this is to keep track of the current step count, this resets its self everytime the motor begins to move again
stepcount = 0

#pins used for direction and step
Direction_Pin = 15
Step_Pin = 13

#set up
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarning(False)

#motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

'''
#mulitplexer setup
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
'''

#move motor up the input amount of steps
#also has queue input to check if there is a STOP command before it moves another step
def raise_the_roof(steps, moto_cmd):
        '''
	if steps == 11160:
		quarter_one = 2790
		quarter_two = 5580
		quarter_three = 8370
		quarter_four = 11159
	elif steps ==15500:
		quarter_one = 3875
		quarter_two = 7750
		quarter_three = 11625
		quarter_four = 15499
	#this takes a picture for every nudge command
	else:
		freq = 1000
	'''
	GPIO.output(Direction_Pin, GPIO.HIGH) #GPIO.HIGH for direction pin means up
	for step in range(steps):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		stepcount = step
		time.sleep(.0036) #.0036 allows for a 1 minute extenstion if input is 16500 (max height)
                '''
		High_Resolution = False
		if (step == quarter_one or step == quarter_two or step == quarter_three or step == quarter_four or step == freq):
			say_cheese_four_times(High_Resolution)
		'''
		cmd = moto_cmd.get_nowait()
		if cmd == 'stop':
			return

#move motor down the input amount of
#also has queue input to check if there is a STOP command before it moves another step
def drop_it_low(steps, moto_cmd):
        '''
	if steps == 11160:
		quarter_one = 2790
		quarter_two = 5580
		quarter_three = 8370
		quarter_four = 11159
	elif steps ==15500:
		quarter_one = 3875
		quarter_two = 7750
		quarter_three = 11625
		quarter_four = 15499
	##this takes 1 picture for every nudge command
	else:
		freq = 1000
	'''
	GPIO.output(Direction_Pin, GPIO.LOW) #GPIO.LOW for direction pin means down
	for step in range(steps):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		stepcount = step
		time.sleep(.0036) #.0036 allows for a 1 minute retraction if input is 16500 (max height)
		'''
		High_Resolution = False
		#TAKE PICTURES AT SPECIFIED FREQUENCY
		if (step == quarter_one or step == quarter_two or step == quarter_three or step == quarter_four or step == freq):
			say_cheese_four_times(High_Resolution)
		'''
		cmd = moto_cmd.get_nowait()
		if cmd == 'stop':
			return
'''
#capture and store image with timestamp
def say_cheese(cam, High_Resolution):
	if High_Resolution == True:
		camera.resolution(1640, 922)
	else:
		camera.resolution(1024, 786)
	timestamp = time.time()
	timestamp = str(timestamp)
	cam = str(cam)
	image = "raspistill -o {:s}.jpg".format(cam+' '+timestamp)
	os.system(image)

#take images from 4 pi cameras
def say_cheese_four_times(High_Resolution):
	#camera A
	GPIO.output(7, False)
	GPIO.output(11, False)
	GPIO.output(12, True)
	say_cheese(1, High_Resolution)
	#camera B
	GPIO.output(7, False)
	GPIO.output(11, False)
	GPIO.output(12, True)
	say_cheese(2, High_Resolution)
	#camera C
	GPIO.output(7, False)
	GPIO.output(11, False)
	GPIO.output(12, True)
	say_cheese(3, High_Resolution)
	#camera D
	GPIO.output(7, False)
	GPIO.output(11, False)
	GPIO.output(12, True)
	say_cheese(4, High_Resolution)
'''

#waits for nudge commands, reset command, or unstuck command from queue,
#as of right now the code will remain in sobering up state until unstuck command is recieved
def sobering_up(moto_cmd):
	##wait for queue (q), if queue has a command then do stuff
	#################################################################MICAH ADD YOUR STUFF HERE################################################
	cmd = moto_cmd.get()
	if cmd == 'reset':
		drop_it_low(16500, moto_cmd)
	if cmd == 'nudge up':
		raise_the_roof(1000, moto_cmd)
	if cmd == 'nudge down':
		drop_it_low(1000, moto_cmd)
	if cmd == 'unstuck':
		is_stuck = False
'''
#complete a minimum success cycle, approximately 72% of max height
def just_scraping_by():
	High_Resolution = False
	say_cheese_four_times(High_Resolution)#capture images directly before moving the motor
	raise_the_roof(11160)
	High_Resolution = True
	say_cheese_four_times(High_Resolution)
	High_Resolution = False
	for i in range(1,9): #remain open for 18 minutes
		time.sleep(120)
		say_cheese_four_times(High_Resolution)
	High_Resolution = True
	say_cheese_four_times(High_Resolution)
	High_Resolution = False
	drop_it_low(11160)
	time.sleep(5)
	say_cheese_four_times(High_Resolution) #take image at end of sustention
	time.sleep(595) #remain closed for 10 minutes
'''

#complete a normal cycle, 100% of max height
def lets_get_as_high_as_we_can():
        '''
	High_Resolution = False
	say_cheese_four_times(High_Resolution)#capture images directly before moving the motor
        '''
	raise_the_roof(15500)
	time.sleep(10)
	'''
	High_Resolution = True
	say_cheese_four_times(High_Resolution)
	High_Resolution = False
	for i in range(1,9): #remain open for 18 minutes
		time.sleep(120)
		
		say_cheese_four_times(High_Resolution)
	High_Resolution = True
	say_cheese_four_times(High_Resolution)
	High_Resolution = False
	'''
	drop_it_low(15500)
	'''
	time.sleep(5)
	say_cheese_four_times(High_Resolution) #take image at end of sustention
	time.sleep(595) #remain closed for 10 minutes
	'''
	time.sleep(8)

def main(run_exp, moto_cmd):
	if(run_exp.is_set()):
                '''
		cycle = 1
		#complete minimum success cycle (2 consectuve successful total)
		while cycle<3:
			if is_stuck == False:
				just_scraping_by()
				#if motor didnt exit early/get stuck in its cycle then increase the cycle count
				if is_stuck == False:
					cycle += 1
			##remains in sobering_up state until commanded that it is unstuck
			while is_stuck == True:
				sobering_up(moto_cmd)
		#complete 100% of max height cycles (any amount after first two successul cycles)
		while cycle>2:
			if is_stuck == False:
				lets_get_as_high_as_we_can()
				#if motor didnt exit early/get stuck in its cycle then increase the cycle count
				if is_stuck == False:
					cycle += 1
				#remains in sobering_up state until commanded that it is unstuck
				while is_stuck == True:
					sobering_up(moto_cmd)
				#########################################################MICAH THIS IS YOU AGAIN FOR TERMINATE EXTENSION CONTRACTION CYCLES ########################
				#cmd = q.no_wait()
				#if cmd == "terminate":	
				if terminate == True:
					return
		'''











                
