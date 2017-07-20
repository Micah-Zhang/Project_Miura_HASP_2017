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

encoder_thread = threading.Thread(target=fmoto.encoder_function, args=(encoder,))
encoder_thread.start()

# To access encoder count, use encoder.get_encoder_count() 

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	cmoto.mission_start_time = time.time() #keep track of mission start time
	while(True):
		fmoto.checkUplink(moto_cmd, downlink)
		if cmoto.top_calib:
			encoder.reset_encoder_count()
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
			if not cmoto.cycle_extending:
				cmoto.cycle_start_time = time.time()
				cmoto.cycle_extending = True
				fmoto.move(int(73*(cmoto.max_step/100) - cmoto.step_count), downlink)
				cmoto.is_raised = True
				cmoto.motor_start_time = time.time()
			elif not cmoto.cycle_contracting and (time.time() > cmoto.motor_start_time + cmoto.top_wait_time):
				cmoto.cycle_contracting = True
				fmoto.move(- cmoto.step_count, downlink)
				cmoto.motor_end_time = time.time()
			elif cmoto.cycle_extending and cmoto.cycle_contracting and cmoto.is_raised and (time.time() > cmoto.motor_end_time + cmoto.bot_wait_time):
				cmoto.cycle_extending = False
				cmoto.cycle_contracting= False
				cmoto.is_raised = False
				cmoto.minimum_success = False
				cmoto.cycle_end_time = time.time()		
		if cmoto.full_extension:
			if not cmoto.cycle_extending:
				cmoto.cycle_start_time = time.time()
				cmoto.cycle_extending = True
				fmoto.move(cmoto.max_step - cmoto.step_count, downlink)
				cmoto.is_raised = True
				cmoto.motor_start_time = time.time()
			elif not cmoto.cycle_contracting and (time.time() > cmoto.motor_start_time + cmoto.top_wait_time):
				cmoto.cycle_contracting = True				
				fmoto.move(- cmoto.step_count, downlink)
				cmoto.motor_end_time = time.time()
			elif cmoto.cycle_extending and cmoto.cycle_contracting and cmoto.is_raised and (time.time() > cmoto.motor_end_time + cmoto.bot_wait_time):
				cmoto.cycle_extending = False
				cmoto.cycle_contracting = False
				cmoto.is_raised = False
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
			fmoto.send_encoder_count(downlink, encoder)
		time.sleep(1)
