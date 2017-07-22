import time
import math
import RPi.GPIO as GPIO
import subprocess as sp
import cama.fcama as fcama

led_pin = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,False)

def main(downlink,cam_is_moving,cam_is_open,cam_reset):
	downlink.put(["CA","BU","CAMA"])
	while True:
		if cam_reset.is_set():
			prev_capture_time = 0
			time_interval = math.inf
			cam_reset.clear()
		if cam_is_moving.is_set():
			time_interval = 5
		if cam_is_open.is_set():
			time_interval = 175
		if time.time() > prev_capture_time + time_interval:
			GPIO.output(led_pin,True)
			sp.call(['python2 /home/pi/miura/cama/fcama.py'], shell=True)
			GPIO.output(led_pin,False)
			prev_capture_time = time.time()
		time.sleep(1)
