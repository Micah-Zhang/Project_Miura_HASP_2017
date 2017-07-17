import time
import moto.cmoto as cmoto
import moto.fmoto as fmoto

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	while(True):
		fmoto.checkUplink(moto_cmd, downlink)
		if cmoto.top_calib:
			fmoto.move(20000)
			cmoto.top_calib = False
			print("top calibrated")
		if cmoto.bot_calib:
			fmoto.move(-20000)
			cmoto.bot_calib = False
			print("bottom calibrated")
		if cmoto.nudge_state:
			fmoto.move(cmoto.nudge_step)
			cmoto.nudge_state = False
		if cmoto.minimum_success:
			if not cmoto.is_raised:
				fmoto.move(int(73*(cmoto.max_step/100) - cmoto.step_count))
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
			'''
			elif cmoto.cycle_count == 1 or cmoto.cycle_count == 2:
				cmoto.cycle_count += 1
				moto_cmd.put(b"\x03")
			elif cmoto.cycle_count > 2:
				cmoto.cycle_count += 1
				moto_cmd.put(b"\x04")
			'''
		time.sleep(1)
