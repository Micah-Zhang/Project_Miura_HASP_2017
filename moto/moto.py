import time
import moto.cmoto as cmoto
import moto.fmoto as fmoto
import RPi.GPIO as GPIO

#gpio setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#motor setup
GPIO.setup(cmoto.Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(cmoto.Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#button setup
GPIO.setup(cmoto.Upper_Button,GPIO.IN)
GPIO.setup(cmoto.Lower_Button,GPIO.IN)

def main(downlink, run_exp, moto_cmd, safe_mode):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	while(True):
		fmoto.checkUplink(moto_cmd, downlink, safe_mode)
		if cmoto.top_calib:
			fmoto.move(20000, downlink, safe_mode)
			cmoto.top_calib = False
			print("top calibrated")
		if cmoto.bot_calib:
			fmoto.move(-20000, downlink, safe_mode)
			cmoto.bot_calib = False
			print("bottom calibrated")
		if cmoto.nudge_state:
			fmoto.move(cmoto.nudge_step, downlink, safe_mode)
			cmoto.nudge_state = False
		if cmoto.minimum_success:
			if not cmoto.cycle_extended:
				cmoto.cycle_start_time = time.time()
				fmoto.move(int(73*(cmoto.max_step/100) - cmoto.step_count), downlink, safe_mode)
				cmoto.motor_start_time = time.time()
				cmoto.cycle_extended = True
				cmoto.is_raised = True
			elif not cmoto.cycle_contracted and (time.time() > cmoto.motor_start_time + cmoto.top_wait_time):
				fmoto.move(- cmoto.step_count, downlink, safe_mode)
				cmoto.motor_end_time = time.time()
				cmoto.cycle_contracted = True
				cmoto.is_raised = False
			elif cmoto.cycle_extended and cmoto.cycle_contracted and (time.time() > cmoto.motor_end_time + cmoto.bot_wait_time):
				cmoto.cycle_extended = False
				cmoto.cycle_contracted = False
				cmoto.minimum_success = False
				cmoto.cycle_end_time = time.time()
		if cmoto.full_extension:
			if not cmoto.cycle_extended:
				cmoto.cycle_start_time = time.time()
				fmoto.move(cmoto.max_step - cmoto.step_count, downlink, safe_mode)
				cmoto.motor_start_time = time.time()
				cmoto.cycle_extended = True
				cmoto.is_raised = True
			elif not cmoto.cycle_contracted and (time.time() > cmoto.motor_start_time + cmoto.top_wait_time):
				fmoto.move(- cmoto.step_count, downlink, safe_mode)
				cmoto.motor_end_time = time.time()
				cmoto.cycle_contracted = True
				cmoto.is_raised = False
			elif cmoto.cycle_extended and cmoto.cycle_contracted and (time.time() > cmoto.motor_end_time + cmoto.bot_wait_time):
				cmoto.cycle_extended = False
				cmoto.cycle_contracted = False
				cmoto.full_extension = False
				cmoto.cycle_end_time = time.time()
		if not cmoto.auto_set and (time.time() > cmoto.mission_start_time + cmoto.auto_wait): #begin automation after set amount of time
			cmoto.auto_set = True
			cmoto.automation = True    
		if cmoto.automation:
			if cmoto.cycle_count == -2:
				cmoto.cycle_count += 1
				moto_cmd.put(b"\x01")
			elif cmoto.cycle_count == -1:
				cmoto.cycle_count += 1
				moto_cmd.put(b"\x02")
			elif cmoto.cycle_count == 0:
				cmoto.cycle_count += 1
				moto_cmd.put(b"\x01")
			elif cmoto.cycle_count == 1 or cmoto.cycle_count == 2:
				if not cmoto.cmd_sent:
					moto_cmd.put(b"\x03")
					cmoto.cmd_sent = True
				elif not cmoto.minimum_success:
					cmoto.cmd_sent = False
					cmoto.cycle_count += 1
					print("cycle count now: ", cmoto.cycle_count)
			elif cmoto.cycle_count > 2:
				if not cmoto.cmd_sent:
					moto_cmd.put(b"\x04")
					cmoto.cmd_sent = True
				elif not cmoto.full_extension:
					cmoto.cmd_sent = False
					cmoto.cycle_count += 1
					print("cycle count is now: ", cmoto.cycle_count)
		if time.time() > cmoto.prev_dwlk_time + 1:
			fmoto.send_step(downlink)
			fmoto.send_step_percent(downlink)
			fmoto.send_button(downlink)
		time.sleep(1)
