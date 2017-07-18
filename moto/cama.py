import moto.fcama as fcama
import moto.cmoto as cmoto
import moto.fmoto as fmoto
import moto.moto as moto

import time

def main(run_exp):
	ms_interval = int(((max_step/4)*.73)-1)
	fe_interval = int((max_step/6)-1)
	tmp_interval = 1
	if cmoto.cycle_extended or cmoto.cycle_contracted:
		if cmoto.step_count == tmp_interval:
			fcama.take_image()
			if minimum_success:
				tmp_interval += ms_interval 
			if full_extension:
				tmp_interval += fe_interval
	if cmoto.is_raised:
		#take an image once per 3 minutes
	if not cmoto.automation:
		#take an image per minute
	if cmoto.image_request:
		#take an image per camera
	
