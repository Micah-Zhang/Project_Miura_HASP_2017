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

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	while(True):
		fmoto.checkUplink(moto_cmd, downlink)
		if cmoto.top_calib:
			fmoto.move(20000, downlink)
			cmoto.top_calib = False
			print("top calibrated")
		if cmoto.bot_calib:
			fmoto.move(-20000, downlink)
			cmoto.bot_calib = False
			print("bottom calibrated")
		if cmoto.nudge_state:
			fmoto.move(cmoto.nudge_step, downlink)
			cmoto.nudge_state = False
		if cmoto.minimum_success:
			if not cmoto.is_raised:
				fmoto.move(int(73*(cmoto.max_step/100) - cmoto.step_count), downlink)
				cmoto.is_raised = True
			elif time.time() > cmoto.cycle_start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count, downlink)
				cmoto.is_raised = False
				cmoto.minimum_success = False
				cmoto.cycle_start_time = 0
				cmoto.cycle_end_time = time.time()
				print("cycle start time reset")
				print("cycle end time set")
		if cmoto.full_extension:
			if not cmoto.is_raised:
				fmoto.move(cmoto.max_step - cmoto.step_count, downlink)
				cmoto.is_raised = True
			elif time.time() > cmoto.cycle_start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count, downlink)
				cmoto.is_raised = False
				cmoto.full_extension = False
				cmoto.cycle_start_time = 0
				cmoto.cycle_end_time = time.time()
				print("cycle start time reset")
				print("cycle end time set")
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
				if not cmoto.cmd_status:
					moto_cmd.put(b"\x03")
					cmoto.cmd_status = True
				elif not cmoto.minimum_success and (time.time() > cmoto.cycle_end_time + cmoto.wait_time):
					cmoto.cmd_status = False
					cmoto.cycle_count += 1
					print("cycle count now: ", cmoto.cycle_count)
			elif cmoto.cycle_count > 2:
				if not cmoto.cmd_status:
					moto_cmd.put(b"\x04")
					cmoto.cmd_status = True
				elif not cmoto.full_extension and (time.time() > cmoto.cycle_end_time + cmoto.wait_time):
					cmoto.cmd_status = False
					cmoto.cycle_count += 1
					print("cycle count is now: ", cmoto.cycle_count)
		if time.time() > cmoto.prev_dwlk_time + 1:
			fmoto.send_step(downlink)
			fmoto.send_step_percent(downlink)
			fmoto.send_button(downlink)
		time.sleep(1)
