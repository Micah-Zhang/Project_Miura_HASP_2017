import time
import serial
import RPi.GPIO as GPIO
import os
import moto.cmoto as cmoto


#move motor
def move(steps, downlink, safe_mode):
	downlink_step = 0
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
		if safe_mode.is_set():
			return
		#stop if moving UP and UP button pressed
		if GPIO.input(cmoto.Upper_Button) and increment == 1:
			print("top button pressed. stopping payload")
			cmoto.max_step = cmoto.step_count
			print("new max step count: ", cmoto.max_step)
			return
		#stop if moving DOWN and DOWN button pressed
		elif GPIO.input(cmoto.Lower_Button) and increment == -1:
			print("botton button pressed. stopping payload")
			cmoto.step_count = 0
			print("step_count reset to: ",cmoto.step_count)
			return
		else:
			GPIO.output(cmoto.Step_Pin, GPIO.HIGH)
			GPIO.output(cmoto.Step_Pin, GPIO.LOW)
			cmoto.step_count += increment
			if downlink_step > 100:
				downlink.put(["MO","SC",str(cmoto.step_count)])
				downlink.put(["MO","SP",'{:.2f}%'.format(cmoto.step_count/cmoto.max_step * 100)])
				lower = GPIO.input(cmoto.Lower_Button)
				upper = GPIO.input(cmoto.Upper_Button)
				downlink.put(["MO","BT",str(lower) + ' ' + str(upper)])
				downlink_step = 0
			else:
				downlink_step += 1
			#time.sleep(.0015) #SANIC MODE (testing)
			time.sleep(.0036) #NANNY MODE (flight)


#parce through the commands
def checkUplink(moto_cmd, downlink, safe_mode, cam_is_moving, cam_is_open, cam_reset):
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
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x04":
				print("setting full_extension flag as TRUE")
				cmoto.full_extension = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x05":
				print("setting automation flag as TRUE")
				cmoto.automation = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x06":
				print("setting automation flag as FALSE")
				cmoto.automation = False
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x07":
				print("entering SAFE MODE")
				cmoto.automation = False
				cmoto.nudge_state = False
				cmoto.minimum_success = False
				cmoto.full_extension = False
				cmoto.cmd_sent = False
				cmoto.cycle_extended = False
				cmoto.cycle_contracted = False
				cmoto.top_calib = False
				cmoto.bot_calib = False
				cmoto.cycle_count -= 1
				cam_is_moving.clear()
				cam_reset.set()
				cam_is_open.set()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x08":
				print("exiting SAFE MODE")
				cam_is_open.clear()
				cam_reset.set()
				cmoto.bot_calib = True
				cmoto.automation = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x09": #reset step count to 0
				print("reset step count = 0")
				cmoto.step_count = 0
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0A": #reset max step to default: 1500
				print("reset max step = 1500")
				cmoto.max_step = 1500
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0B": #set is_open to false
				cam_is_open.clear()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0C": #set is_open to true
				cam_is_open.set()
				downlink.put(["MO","AK",packet])
			else:
				downlink.put(["MO","ER",packet])
		elif type(cmd) is int:
			packet = cmd
			downlink.put(["MO","AK",packet])
			if abs(cmd) <= 100:
				#cmoto.nudge_step = ((cmd/100)-(cmoto.step_count/cmoto.max_step))*cmoto.max_step)
				cmoto.nudge_step = int((cmd*(cmoto.max_step/100)) - cmoto.step_count)
				print("nudge_step defined")
				cmoto.nudge_state = True #signal ready for nudging
				print("setting nudge_state flag a TRUE")
				downlink.put(["MO","AK",str(cmd)])
			elif abs(cmd) > 100 and abs(cmd) < 202:
				if cmd > 0:
					cmd -= 101
					cmoto.nudge_step = int(cmd*(cmoto.max_step/100))
					cmoto.nudge_state = True #signal ready for nudging
					downlink.put(["MO","AK",str(cmd)])
				else:
					cmd += 101
					cmoto.nudge_step = int(cmd*(cmoto.max_step/100))
					cmoto.nudge_state = True #signal ready for nudging
					downlink.put(["MO","AK",str(cmd)])
			elif abs(cmd) >= 202:
				cmd -= 204
				cmoto.cycle_count = cmd
				print("changed cycle count to: ", cmoto.cycle_count)
			else:
				downlink.put(["MO", "ER",str(cmd)])
