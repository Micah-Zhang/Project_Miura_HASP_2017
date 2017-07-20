import time
import serial
import RPi.GPIO as GPIO
import os
import moto.cmoto as cmoto


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
		encoder_data = []
		for i in range(100): # So we're not constantly accessing the file]
			for i in range(100):
				time.sleep(.00005)
				encoder.process_pulse()
			encoder_data.append((time.time(), encoder.get_encoder_count()))
		with open('encoder_data.txt','a+') as f:
			for line in encoder_data:
				f.write('{} {}\n'.format(line[0], line[1]))

#move motor
def move(steps, downlink):
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
			cmoto.current_percent = cmoto.step_count/cmoto.max_step #track percentage extended
			#send_step(downlink)
			#send_step_percent(downlink)
			#send_button(downlink)
			time.sleep(0.0015)
			#time.sleep(.0036) #change to this for systems test

def send_step(downlink): #downlink step count" 
	try:
		downlink.put(["MO","SC",str(cmoto.step_count)])
	except:
		pass

def send_step_percent(downlink): #downlink percent deployment
	try:
		downlink.put(["MO","SP",str(cmoto.current_percent)])
	except:
		pass

def send_encoder_count(downlink, encoder): #downlink quantized encoder angular displacement 
	try:
		downlink.put(["MO","EC",str(encoder.get_encoder_count())])
	except:
		pass

def send_button(downlink):
	try:
		data = []
		data.append(int(GPIO.input(cmoto.Lower_Button)))
		data.append(int(GPIO.input(cmoto.Upper_Button)))
		downlink.put(["MO","BT",cs_str(data)])
	except:
		pass


def cs_str(data):
	out = ""
	for i in range(len(data)):
		out += "%f " % (data[i])
	return out

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
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x04":
				print("setting full_extension flag as TRUE")
				cmoto.full_extension = True
				downlink.put(["MO","AK",packet])
			elif cmd == b"\x05":
				print("setting automation flag as TRUE")
				cmoto.automation = True
				print("set automation flag as TRUE")
				downlink.put(["MO","AK",packet])
				print("sent acknowledgement command")
			elif cmd == b"\x06":
				print("setting automation flag as FALSE")
				cmoto.automation = False
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
