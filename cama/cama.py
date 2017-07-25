import time
import RPi.GPIO as GPIO
import os

led_pin = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,False)

def take_image():
	try:
		os.system('fswebcam -q -i 0 -d /dev/video0 -r 1024x768 -S 10 /home/pi/images/cam0/{:.0f}.jpg'.format(time.time()))
		status = "1 "
	except:
		status = "0 "
	try:
		os.system('fswebcam -q -i 0 -d /dev/video1 -r 1024x768 -S 10 /home/pi/images/cam1/{:.0f}.jpg'.format(time.time()))
		status += "1 "
	except:
		status += "0 "
	try:
		os.system('fswebcam -q -i 0 -d /dev/video2 -r 1024x768 -S 10 /home/pi/images/cam2/{:.0f}.jpg'.format(time.time()))
		status += "1 "
	except:
		status += "0 "
	try:
		os.system('fswebcam -q -i 0 -d /dev/video3 -r 1024x768 -S 10 /home/pi/images/cam3/{:.0f}.jpg'.format(time.time()))
		status += "1"
	except:
		status.append(0)
		status += "0"
	return status

def main(downlink,cam_is_moving,cam_is_open,cam_reset):
	downlink.put(["CA","BU","CAMA"])
	prev_capture_time = 0
	time_interval = float("inf")
	while True:
		if cam_reset.is_set():
			prev_capture_time = 0
			time_interval = float("inf")
			cam_reset.clear()
		if cam_is_moving.is_set():
			time_interval = 2
		if cam_is_open.is_set():
			time_interval = 175
		if time.time() > prev_capture_time + time_interval:
			GPIO.output(led_pin,True)
			downlink.put(['CA','IM',take_image()])
			GPIO.output(led_pin,False)
			prev_capture_time = time.time()
		time.sleep(1)
