import time
import serial
import RPi.GPIO as GPIO
import os
import moto.cmoto as cmoto

#move motor
def move(steps):
	#determine if moving up or down. respond accordingly.
	if steps > 0:
		print("ready to move up")
		GPIO.output(cmoto.Direction_Pin, GPIO.HIGH)
		increment = 1
	else:
		print("ready to move down")
		GPIO.output(cmoto.Direction_Pin, GPIO.LOW)
		increment = -1
	steps = abs(steps)
	for step in range(steps):
		#stop moving if either button depressed
		if GPIO.input(cmoto.Upper_Button) or GPIO.input(cmoto.Lower_Button):
			if GPIO.input(cmoto.Upper_Button): #figure out which button was pressed and then reset stepcount accordingly
				print("Upper button pressed")
				cmoto.max_step = cmoto.step_count
				print("max step now: ", cmoto.max_step)
			else:
				print("Lower button pressed")
				cmoto.step_count = 0
				print("step count now: ", cmoto.step_count)
			return
		print("moving motor")
		GPIO.output(cmoto.Step_Pin, GPIO.HIGH)
		GPIO.output(cmoto.Step_Pin, GPIO.LOW)
		cmoto.step_count += increment
		cmoto.current_percent = cmoto.step_count/cmoto.max_step
		time.sleep(.0036)

		'''
		#stop if moving UP and UP button pressed
		if GPIO.input(cmoto.Upper_Button) and increment == 1:
			print("top button pressed. stopping payload")
			cmoto.max_step = cmoto.step_count
			return
		#stop if moving DOWN and DOWN button pressed
		elif GPIO.input(cmoto.Lower_Button) and increment == -1:
			print("botton button pressed. stopping payload")
			cmoto.step_count = 0
			return
		#otherwise, move motor and increase step count
		else:
			print("moving motor")
			GPIO.output(cmoto.Step_Pin, GPIO.HIGH)
			GPIO.output(cmoto.Step_Pin, GPIO.LOW)
			cmoto.step_count += increment
			cmoto.current_percent = cmoto.step_count/cmoto.max_step #track percentage extended
			time.sleep(.0036)
		'''

#take image from all four cameras and save with the current timestamp as the name
def take_4_images():
	print("Taking image") #placeholder until cameras work
	'''
	for camera in range(1,4):
        	timestamp = "{0:.2f}".format(time.time())
        	os.system('fswebcam -r 1080x720 -d /dev/video{}.format(str(camera-1)) --save {}.jpg'.format(timestamp))  
	'''

#parce through the commands
def checkUplink(moto_cmd, downlink):
	while not moto_cmd.empty(): #grab commands until queue empty
		cmd = moto_cmd.get()
		print("command received")
		if type(cmd) is bytes:
			packet = hex(int.from_bytes(cmd, byteorder='big'))
			if cmd == b"\x01":
				print("setting bot_calib flag as TRUE")
				cmoto.bot_calib = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x02":
				print("setting top_calib flag as TRUE")
				cmoto.top_calib = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x03":
				print("setting minimum_success flag as TRUE")
				cmoto.minimum_success = True
				cmoto.cycle_start_time = time.time()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x04":
				print("setting full_extension flag as TRUE")
				cmoto.full_extension = True
				cmoto.cycle_start_time = time.time()
				downlink.put(["MO","AK",packet])
			else:
				downlink.put(["MO","ER",packet])
		elif type(cmd) is int:
			packet = cmd
			downlink.put(["MO","AK",packet])
			if abs(cmd) <= 100:
				#cmoto.nudge_step = ((cmd/100)-(cmoto.step_count/cmoto.max_step))*cmoto.max_step)
				cmoto.nudge_step = (cmd*(cmoto.max_step/100)) - cmoto.step_count
				print("nudge_step defined")
				cmoto.nudge_state = True #signal ready for nudging
				print("setting nudge_state flag a TRUE")
				downlink.put(["MO","AK",str(cmd)])
			elif abs(cmd) > 100:
				cmd = cmd - 101
				cmoto.nudge_step = cmd*(cmoto.max_step/100)
				print("nudge_step defined")
				cmoto.nudge_state = True #signal ready for nudging
				print("setting nudge_state flag as TRUE")
				downlink.put(["MO","AK",str(cmd)])
			else:
				downlink.put(["MO", "ER",str(cmd)])
