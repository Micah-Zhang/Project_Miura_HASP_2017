#import moto.fcama as fcama
import moto.cmoto as cmoto
import moto.fmoto as fmoto
import moto.moto as moto

import time

def main(run_exp):
	ms_interval = int(((cmoto.max_step*.73)/4)-1)
	fe_interval = int((cmoto.max_step/6)-1)
	open_interval = 180
	while True:
		tmp_open_interval = 0
		tmp_step_interval = cmoto.step_count
		#during extending and contracting stages, frequency is dependant on steps
		while cmoto.cycle_extended:
			if cmoto.step_count > tmp_step_interval:
				print('taking extending images')			
				fcama.take_image()	
				if minimum_success:
					tmp_step_interval += ms_interval 
				elif full_extension:
					tmp_step_interval += fe_interval
				else:
					tmp_step_interval += 2500
		while cmoto.cycle_contracted:
			if cmoto.step_count < tmp_step_interval:
				print('taking contracting images')
				fcama.take_image()
				if minimum_success:
					tmp_step_interval -= ms_interval 
				elif full_extension:
					tmp_step_interval -= fe_interval
				else:
					tmp_step_interval -= 2500
		#during open, frequency is dependant on time	
		start_time = time.time()
		while cmoto.is_raised:
			temp_time = time.time()
			if temp_time > (start_time + temp_open_interval):
				print('taking open images')			
				fcama.take_image()
				temp_open_interval += open_interval
				
			

