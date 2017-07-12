import time
import fmoto
import cmoto

def main(downlink, run_exp, moto_cmd):
	downlink.put(["MO","BU","MOTO"]) #verify succesful thread start
	while(True):
		fmoto.checkUplink(moto_cmd)
		time.sleep(1)
