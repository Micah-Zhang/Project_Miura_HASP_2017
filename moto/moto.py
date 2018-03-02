'''
    ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/
'''

import time
import moto.cmoto as cmoto
import moto.fmoto as fmoto
import RPi.GPIO as GPIO
import threading

#gpio setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#motor setup
GPIO.setup(cmoto.Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(cmoto.Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#button setup
GPIO.setup(cmoto.Upper_Button,GPIO.IN)
GPIO.setup(cmoto.Lower_Button,GPIO.IN)

# Encoder initialization
pin_A = 18
pin_B = 16
GPIO.setup(pin_A, GPIO.IN)
GPIO.setup(pin_B, GPIO.IN)
encoder = fmoto.Encoder(pin_A, pin_B)

# To access encoder count, use encoder.get_encoder_count()

encoder_thread = threading.Thread(target=fmoto.encoder_function, args=(encoder,))
encoder_thread.start()

def main(downlink, moto_cmd, safe_mode, cam_is_moving, cam_is_open, cam_reset):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	# Make sure camera is off
	cam_reset.set()
	while(True):
		# Check for any Uplink Commands
		fmoto.checkUplink(moto_cmd, downlink, safe_mode, cam_is_moving, cam_is_open, cam_reset)
		# If top calibration flag queued
		if cmoto.top_calib:
			# Stop current camera operation
			cam_is_open.clear()
			cam_reset.set()
			# Begin camera operation with high frequency image capture
			cam_is_moving.set()
			# Move motor up 16000 steps
			fmoto.move(16000, downlink, safe_mode, encoder)
			# Reset camera
			cam_is_moving.clear()
			cam_reset.set()
			# Begin low frequency image capture
			cam_is_open.set()
			# Reset top_calib flag
			cmoto.top_calib = False
			print("top calibrated")
		# If bottom calibration flag queued
		if cmoto.bot_calib:
			# Reset camera
			cam_is_open.clear()
			cam_reset.set()
			# Start high frequency camera capture
			cam_is_moving.set()
			# Move motor down 16000 steps
			fmoto.move(-16000, downlink, safe_mode, encoder)
			# Reset camera
			cam_is_moving.clear()
			# Begin low frequency image capture
			cam_reset.set()
			# Reset bot_calib flag
			cmoto.bot_calib = False
			print("bottom calibrated")
		# If nudge command queued
		if cmoto.nudge_state:
			# Reset camera
			cam_is_open.clear()
			cam_reset.set()
			# Begin high frequency camera capture
			cam_is_moving.set()
			# Nudge motor up or down specified amount
			fmoto.move(cmoto.nudge_step, downlink, safe_mode, encoder)
			# Reset camera
			cam_is_moving.clear()
			cam_reset.set()
			# Reset nudge_state flag
			cmoto.nudge_state = False
		# If either a minimum success or full extension cycle is queued
		if cmoto.minimum_success or cmoto.full_extension:
			# If the payload isn't already extended
			if not cmoto.cycle_extended:
				# Reset camera
				cam_is_open.clear()
				cam_reset.set()
				# Begin high frequency camera capture
				cam_is_moving.set()
				# Store cycle start time
				cmoto.cycle_start_time = time.time()
				# If minimum success, make sure to move to 70% max height
				if cmoto.minimum_success:
					fmoto.move(int(73*(cmoto.max_step/100) - cmoto.step_count), downlink, safe_mode, encoder)
				# Otherwise move to max height
				else:
					fmoto.move(cmoto.max_step - cmoto.step_count + 750, downlink, safe_mode, encoder)
				# Grab current time
				cmoto.motor_start_time = time.time()
				# Reset camera
				cam_is_moving.clear()
				cam_reset.set()
				# Begin low frequency camera capture
				cam_is_open.set()
				# Prevent Part 1 of cycle from executing again until all other steps passed
				cmoto.cycle_extended = True
			# If the payload is extended and 18 minutes has passed
			elif not cmoto.cycle_contracted and (time.time() > cmoto.motor_start_time + cmoto.top_wait_time):
				# Reset the camera
				cam_is_open.clear()
				cam_reset.set()
				# Begin high frequency camera capture
				cam_is_moving.set()
				# Move down to 0% max height
				fmoto.move(- cmoto.step_count - 750, downlink, safe_mode, encoder)
				# Grab current time
				cmoto.motor_end_time = time.time()
				# Reset camera
				cam_is_moving.clear()
				cam_reset.set()
				# Prevent Part 2 of cycle from executing again until all other steps passed
				cmoto.cycle_contracted = True
			# If the payload is contracted and 10 minutes has passed
			elif cmoto.cycle_extended and cmoto.cycle_contracted and (time.time() > cmoto.motor_end_time + cmoto.bot_wait_time):
				# Reset all flags allowing for cycle to restart
				cmoto.cycle_extended = False
				cmoto.cycle_contracted = False
				cmoto.minimum_success = False
				# This line is extraneous. Originally, it was supposed to used for camera operation.
				cmoto.cycle_end_time = time.time()
		# Automatically begins automation after specified time passes
		if not cmoto.auto_set and (time.time() > cmoto.mission_start_time + cmoto.auto_wait): #begin automation after set amount of time
			# Prevent automation from beginning automatically again
			cmoto.auto_set = True
			# Queue automation
			cmoto.automation = True
		# If automation has been queued
		if cmoto.automation:
			# The first 3 cycles are calibration cycles (down up down) to make sure full extension cycle begins at bottom
			if cmoto.cycle_count == -2:
				cmoto.cycle_count += 1
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				# Queue bottom calibration cycle
				moto_cmd.put(b"\x01")
			elif cmoto.cycle_count == -1:
				cmoto.cycle_count += 1
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				# Queue top calibration cycle
				moto_cmd.put(b"\x02")
			elif cmoto.cycle_count == 0:
				cmoto.cycle_count += 1
				downlink.put(["MO","CC",str(cmoto.cycle_count)])
				# Queue bottom calibration cycle
				moto_cmd.put(b"\x01")
			# Once the calibration cycles are finished, run full extension cycles until the mission ends
			elif cmoto.cycle_count > 0:
				# If a full extension cycle hasn't already been queued
				if not cmoto.cmd_sent:
					# Queue full extension cycle
					moto_cmd.put(b"\x04")
					cmoto.cmd_sent = True
				# Once the full extension cycle is finished
				elif not cmoto.full_extension:
					# Reset the cmd_sent flag
					cmoto.cmd_sent = False
					cmoto.cycle_count += 1
					# Downlink the new cycle count
					downlink.put(["MO","CC",str(cmoto.cycle_count)])
		# Every second downlink the step count, step count percentage, button statuses, and encoder count
		downlink.put(["MO","SC",str(cmoto.step_count)])
		downlink.put(["MO","SP",'{:.2f}%'.format(cmoto.step_count/cmoto.max_step * 100)])
		lower = GPIO.input(cmoto.Lower_Button)
		upper = GPIO.input(cmoto.Upper_Button)
		downlink.put(["MO","BT",str(lower) + ' ' + str(upper)])
		downlink.put(["MO","EC",str(encoder.get_encoder_count())])
		time.sleep(1)
