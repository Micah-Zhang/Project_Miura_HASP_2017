import time
import serial
import RPi.GPIO as GPIO
import os
import cmoto

#move motor
def move(steps):
	#determine if moving up or down. respond accordingly.
	if steps > 0:
		GPIO.output(cmoto.Direction_Pin, GPIO.HIGH)
		increment = 1
	else:
		GPIO.output(cmoto.Direction_Pin, GPIO.LOW)
		increment = -1
	for step in range(steps):
		#stop moving if either button depressed
		if GPIO.input(cmoto.Upper_Button)|GPIO.input(cmoto.Lower_Button):
			return
		#otherwise, move motor and increase step count
		GPIO.output(cmoto.Step_Pin, GPIO.HIGH)
		GPIO.output(cmoto.Step_Pin, GPIO.LOW)
		cmoto.step_count += increment
		cmoto.current_percent = cmoto.step_count/cmoto.max_step #track percentage extended
		time.sleep(.0036)

#take image from all four cameras and save with the current timestamp as the name
def take_4_images():
	print("Taking image") #placeholder until cameras work
	'''
	for camera in range(1,4):
        	timestamp = "{0:.2f}".format(time.time())
        	os.system('fswebcam -r 1080x720 -d /dev/video{}.format(str(camera-1)) --save {}.jpg'.format(timestamp))  
	'''

#parce through the commands
def checkUplink(moto_cmd):
	while not moto_cmd.empty(): #grab commands until queue empty
		cmd = moto_cmd.get()
		if type(cmd) is bytes:
			packet = hex(int.from_bytes(cmd, byteorder='big'))
			if cmd == b"\x01":
				cmoto.bot_calib = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x02":
				cmoto.top_calib = True
				downlink.put(["MO","AK",packet])
			else:
				downlink.put(["MO","ER",packet])
		elif type(cmd) is int:
			packet = cmd
			downlink.put(["MO","AK",packet])
			if abs(cmd) <= 100: # cmd = (0,100) => (0, 17500)
				#cmoto.nudge_step = ((cmd/100)-(cmoto.step_count/cmoto.max_step))*cmoto.max_step)
				cmoto.nudge_step = (cmd*(cmoto.max_step/100)) - cmoto.step_count
				cmoto.nudge_state = True #signal ready for nudging
				downlink.put(["MO","AK",str(cmd)])
			elif abs(cmd) > 100: # cmd = (101, 201)
				cmd = cmd - 101
				cmoto.nudge_step = cmd*(cmoto.max_step/100)
				cmoto.nudge_state = True #signal ready for nudging
				downlink.put(["MO","AK",str(cmd)])
			else:
				downlink.put(["MO", "ER",str(cmd)])
