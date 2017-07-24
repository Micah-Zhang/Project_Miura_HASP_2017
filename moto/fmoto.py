import time
import serial
import RPi.GPIO as GPIO
import os
import moto.cmoto as cmoto


#move motor
def move(steps, downlink, safe_mode, encoder):
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
			encoder.reset_encoder_count()
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
				downlink.put(["MO","EC",str(encoder.get_encoder_count())])
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
				print("querying safe mode")
				downlink.put(["MO","AK",packet])
				if safe_mode.is_set():
					downlink.put(["MO","SM","ON"])
				else:
					downlink.put(["MO","SM","OFF"])
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
				if cmoto.cycle_count < -2:
					cmoto.cycle_count = -2
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				cam_is_moving.clear()
				cam_reset.set()
				cam_is_open.set()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x08":
				print("exiting SAFE MODE")
				cam_is_open.clear()
				cam_reset.set()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x09": #reset step count to 0
				print("reset step count = 0")
				cmoto.step_count = 0
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0A": #reset max step to default: 16000
				print("reset max step = 16000")
				cmoto.max_step = 16000
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0B": #query is_open
				print("querying is open")
				downlink.put(["MO","AK",packet])
				if cam_is_open.is_set():
					downlink.put(["MO","IO","ON"])
				else:
					downlink.put(["MO","IO","OFF"])
			elif cmd == b"\x0C": #set is_open to false
				cam_is_open.clear()
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x0D": #set is_open to true
				cam_is_open.set()
				downlink.put(["MO","AK",packet])
			else:
				downlink.put(["MO","ER",packet])
		elif type(cmd) is int:
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
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				downlink.put(["MO","AK",str(cmd)])
			else:
				downlink.put(["MO", "ER",str(cmd)])

class Encoder:
	def __init__(self, pin_A=18, pin_B=16):
		self.pin_A = pin_A
		self.pin_B = pin_B

		self.encoder_count = 0

		self.pin_A_last_state = GPIO.input(self.pin_A)

		return

	def process_pulse(self):
		pin_A_state = GPIO.input(self.pin_A)

		# If states are different, that means a pulse has occured
		if self.pin_A_last_state != pin_A_state:
			# If the output of B is different to output of A, encoder is moving down
			if GPIO.input(self.pin_B) == pin_A_state:
				self.encoder_count += 1
			else:
				self.encoder_count -= 1
		self.pin_A_last_state = pin_A_state

		return

	def get_encoder_count(self):
		return self.encoder_count

	def reset_encoder_count(self):
		self.encoder_count = 0
		return

def encoder_function(encoder):
	while True:
		time.sleep(.00005)
		encoder.process_pulse()
		encoder_data = []

