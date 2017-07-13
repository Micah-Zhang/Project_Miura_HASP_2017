import time
import fmoto
import cmoto

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	while(True):
		fmoto.checkUplink(moto_cmd)
		time.sleep(1)
		if top_calib:
			fmoto.move(20000)
			cmoto.top_calib = False
		if bot_calib:
			fmoto.move(-20000)
			cmoto.bot_calib = False
		if cmoto.nudge_state:
			fmoto.move(cmoto.nudge_step)
			cmoto.nudge_state = False
		if cmoto.minimum_success:
			if not cmoto.is_raised:
				fmoto.move(73*(cmoto.max_step/100) - cmoto.step_count)
				cmoto.is_raised = True
			elif time.time() > cmoto.start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count)
				cmoto.is_raised = False
				cmoto.minimum_success = False
		if cmoto.full_extension:
			if not cmoto.is_raised:
				fmoto.move(cmoto.max_step - cmoto.step_count)
				cmoto.is_raised = True
			elif time.time() > cmoto.start_time + cmoto.wait_time:
				fmoto.move(- cmoto.step_count)
				cmoto.is_raised = False
				cmoto.full_extenion = False
