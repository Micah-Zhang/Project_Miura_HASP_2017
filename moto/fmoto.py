import time
import serial
import RPi.GPIO as GPIO
import os
import moto.cmoto as cmoto


# "move" function:
# Takes steps to be moved, downlink queue, safe_mode flag, and encoder class as inputs. No outputs.
# Moves motor specified number of steps. Will move until either the specified step count is reached or the respective button is pressed
# Keeps track of and downlinks stepcount, stepcount percentage, button state, and encoder count every 100 steps
# Stops/will not begin moving if safe_mode flag is true
def move(steps, downlink, safe_mode, encoder):
	# Enables downlink every 100 steps. Resets to 0 after every downlink.
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
		# Allows near immediate response when in safe mode
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
			# Move 1 step
			GPIO.output(cmoto.Step_Pin, GPIO.HIGH)
			GPIO.output(cmoto.Step_Pin, GPIO.LOW)
			# Update step count variable accordingly
			cmoto.step_count += increment
			# Every 100 steps
			if downlink_step > 100:
				# Downlink current step count
				downlink.put(["MO","SC",str(cmoto.step_count)])
				# Calculate step count percentage (current step/max step) downlink
				downlink.put(["MO","SP",'{:.2f}%'.format(cmoto.step_count/cmoto.max_step * 100)])
				# Retrieve upper and lower button states
				lower = GPIO.input(cmoto.Lower_Button)
				upper = GPIO.input(cmoto.Upper_Button)
				# Downlink button states
				downlink.put(["MO","BT",str(lower) + ' ' + str(upper)])
				# Downlink encoder count
				downlink.put(["MO","EC",str(encoder.get_encoder_count())])
				downlink_step = 0
			else:
				downlink_step += 1
			#time.sleep(.0015) #SANIC MODE (testing)
			time.sleep(.0036) #NANNY MODE (flight)


# function: checkUplink
# Takes moto_cmd flag, downlink queue, safe_mode flag, cam_is_moving flag, cam_is_open flag, and cam_reset flag as inputs. No outputs.
# Takes all commands received from uplink thread and responds accordingly
def checkUplink(moto_cmd, downlink, safe_mode, cam_is_moving, cam_is_open, cam_reset):
	while not moto_cmd.empty(): #grab commands until queue empty
		cmd = moto_cmd.get()
		print("command received")
		# Function is passed either bytes or integers which is used to parse command
		if type(cmd) is bytes:
			# Store packet for downlink
			packet = hex(int.from_bytes(cmd, byteorder='big'))
			# Sets bottom calibration flag to true and downlinks acknowledgement
			if cmd == b"\x01":
				print("setting bot_calib flag as TRUE")
				cmoto.bot_calib = True
				downlink.put(["MO","AK",packet])
			# Sets top calibration flag to true and downlinks acknowledgement
			elif cmd == b"\x02":
				print("setting top_calib flag as TRUE")
				cmoto.top_calib = True
				downlink.put(["MO","AK",packet])
			# Sets minimum success flag to true and downlinks acknowledgement
			elif cmd == b"\x03":
				print("setting minimum_success flag as TRUE")
				cmoto.minimum_success = True
				downlink.put(["MO","AK",packet])
			# Sets full extension flag to true and downlinks acknowledgement
			elif cmd == b"\x04":
				print("setting full_extension flag as TRUE")
				cmoto.full_extension = True
				downlink.put(["MO","AK",packet])
			# Sets automation flag to true and downlinks acknowledgement
			elif cmd == b"\x05":
				print("setting automation flag as TRUE")
				cmoto.automation = True
				downlink.put(["MO","AK",packet])
			# Determines of is safe of is on or off and downlinks safe mode status
			elif cmd == b"\x06":
				print("querying safe mode")
				downlink.put(["MO","AK",packet])
				if safe_mode.is_set():
					downlink.put(["MO","SM","ON"])
				else:
					downlink.put(["MO","SM","OFF"])
			# Turns on safe mode, which turns OFF all flags that could induce movement
			elif cmd == b"\x07":
				print("entering SAFE MODE")
				# Prevents automation conditional from repeating
				cmoto.automation = False
				# Stops nudge_state conditional from repeating
				cmoto.nudge_state = False
				# Stops minimum_success conditional from repeating
				cmoto.minimum_success = False
				# Prevents full_extension conditional from repeating
				cmoto.full_extension = False
				# If code is still inside full_extension or min_success cycle, forces it to exit
				cmoto.cmd_sent = False
				# Forces program to exit out of main cycle
				cmoto.cycle_extended = False
				# Forces program to exit out of main cycle
				cmoto.cycle_contracted = False
				# If a top calibration cycle was queued, remove it from the queue
				cmoto.top_calib = False
				# If a bottom calibration cycle was queued, remove it from the queue
				cmoto.bot_calib = False
				# Automatically revert to previous cycle after exiting safe mode
				cmoto.cycle_count -= 1
				# Unless cycle count is already a minimum, then just set cycle count to default, -2, or the first calibration cycle
				if cmoto.cycle_count < -2:
					cmoto.cycle_count = -2
				# Downlink the new cycle count
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				# Stop all current camera operation. Enter "observation mode" characterized by lower frequency of image capture
				cam_is_moving.clear()
				cam_reset.set()
				cam_is_open.set()
				downlink.put(["MO","AK",packet])
			# Exit safe mode. Exit observation mode.
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
			# Query observation mode status.
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
			# Send error message
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

