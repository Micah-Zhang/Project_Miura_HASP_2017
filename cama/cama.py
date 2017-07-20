import subprocess as sp
import os
import moto.cmoto as cmoto
import time
import threading

def main():
	ms_interval = int(((cmoto.max_step*.73)/4)-1000)
	fe_interval = int((cmoto.max_step/6)-1000)
	open_interval = 180
	while True:
		if not cmoto.auto_set and (time.time() > cmoto.mission_start_time + cmoto.auto_wait): 
			while True:
				time.sleep(1)
				tmp_open_interval = 0
				tmp_step_interval = cmoto.step_count
				#during extending and contracting stages, frequency is dependant on steps
				print("extended? ", cmoto.cycle_extending)
				print("contracted? ", cmoto.cycle_contracting)
				print("is raised? ", cmoto.is_raised)
				print("min succes? ", cmoto.minimum_success)
				print("full extension? ", cmoto.full_extension)
				if cmoto.cycle_extending and not cmoto.is_raised and not cmoto.bot_calib and not cmoto.top_calib:
					time.sleep(1)
					if cmoto.step_count > tmp_step_interval:
						print('taking extending images')			
						sp.call(['python2 /home/pi/miura/cama/fcama.py'], shell=True)
						if cmoto.minimum_success:
							tmp_step_interval += ms_interval 
						elif cmoto.full_extension:
							tmp_step_interval += fe_interval
						else:
							tmp_step_interval += 2500
				tmp_step_interval = cmoto.step_count
				if cmoto.cycle_contracting and not cmoto.bot_calib and not cmoto.top_calib:
					time.sleep(1)					
					if cmoto.step_count < tmp_step_interval:
						print('taking contracting images')
						sp.call(['python2 /home/pi/miura/cama/fcama.py'], shell=True)
						if cmoto.minimum_success:
							tmp_step_interval -= ms_interval 
						elif cmoto.full_extension:
							tmp_step_interval -= fe_interval
						else:
							tmp_step_interval -= 2500
				#during open, frequency is dependant on time	
				start_time = time.time()
				while cmoto.is_raised  and not cmoto.cycle_contracting and not cmoto.bot_calib and not cmoto.top_calib:
					time.sleep(1)
					temp_time = time.time()
					if temp_time > (start_time + tmp_open_interval):
						print('taking open images')		
						sp.call(['python2 /home/pi/miura/cama/fcama.py'], shell=True)
						tmp_open_interval += open_interval
			
if __name__ == '__main__':
	main()	

