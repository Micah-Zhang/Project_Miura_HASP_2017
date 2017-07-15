import time
import moto.cmoto as cmoto
import moto.fmoto as fmoto

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	while(True):
		fmoto.checkUplink(moto_cmd)
		if cmoto.top_calib:
			fmoto.move(20000)
			cmoto.top_calib = False
		if cmoto.bot_calib:
			fmoto.move(-20000)
			cmoto.bot_calib = False
		if cmoto.nudge_state:
			fmoto.move(cmoto.nudge_step)
			cmoto.nudge_state = False
		if cmoto.minimum_success:
			if not cmoto.is_raised:
				fmoto.move(73*(cmoto.max_step/100) - cmoto.step_count)
				cmoto.is_raised = True
			elif time.time() > cmoto.cycle_start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count)
				cmoto.is_raised = False
				cmoto.minimum_success = False
		if cmoto.full_extension:
			if not cmoto.is_raised:
				fmoto.move(cmoto.max_step - cmoto.step_count)
				cmoto.is_raised = True
			elif time.time() > cmoto.cycle_start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count)
				cmoto.is_raised = False
				cmoto.full_extension = False
'''
		if cmoto.automation:
			moto_cmd.put(b"\x01") #calibrate motor at bottom
			moto_cmd.put(b"\x02") #calibrate motor at top
			moto_cmd.put(b"\x03") #complete minimum success cycle
			moto_cmd.put(b"\x03") #complete minimum success cycle
			moto_cmd.put(b"\x04") #complete full extension cycle
		time.sleep(1)
'''
