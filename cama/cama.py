import time
import RPi.GPIO as GPIO
import os

led_pin = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,False)

# This function is used to take images from each one of the four cameras. It contains try and except statements to prevent the code from getting "stuck". Not completely sure if its actuall useful, however.
# Inputs: None
# Outputs: If all images taken successfully, returns string "1 1 1 1". If a camera fails, replace the 1 with a 0.
def take_image():
	# Take image using 1st camera
	try:
		os.system('fswebcam -q -i 0 -d /dev/video0 -r 1024x768 -S 10 /home/pi/images/cam0/{:.0f}.jpg'.format(time.time()))
		status = "1 "
	except:
		status = "0 "
	# Take image using 2nd camera
	try:
		os.system('fswebcam -q -i 0 -d /dev/video1 -r 1024x768 -S 10 /home/pi/images/cam1/{:.0f}.jpg'.format(time.time()))
		status += "1 "
	except:
		status += "0 "
	# Take image using 3rd camera
	try:
		os.system('fswebcam -q -i 0 -d /dev/video2 -r 1024x768 -S 10 /home/pi/images/cam2/{:.0f}.jpg'.format(time.time()))
		status += "1 "
	except:
		status += "0 "
	# Take image using 4th camera
	try:
		os.system('fswebcam -q -i 0 -d /dev/video3 -r 1024x768 -S 10 /home/pi/images/cam3/{:.0f}.jpg'.format(time.time()))
		status += "1"
	except:
		status.append(0)
		status += "0"
	return status

# This function controls general camera operation. Everything is contained within a single while loop.
def main(downlink,cam_is_moving,cam_is_open,cam_reset):
	downlink.put(["CA","BU","CAMA"])
	prev_capture_time = 0
	# Setting the time interval = infinity prevents the camera from taking images
	time_interval = float("inf")
	# Main loop that controls camera operation. The cornerstone of the camera operation is the "time_interval" variable.
	# Set to inf to prevent image capture. Or chance to 2 seconds or 175 seconds based on desired capture frequency.
	while True:
		# Reset camera timing variables
		if cam_reset.is_set(): # To stop camera operation, set cam_is_open and cam_is_moving to false and set cam_reset to True
			prev_capture_time = 0
			time_interval = float("inf") # Stops camera operation
			cam_reset.clear()
		# Set time interval to be 2 seconds to take images more frequently when the motor is moving
		if cam_is_moving.is_set():
			time_interval = 2
		# Set time interval to be 175 seconds to take images less frequently when the motor is not moving
		if cam_is_open.is_set():
			time_interval = 175
		# This is the main camera operation conditional. It both calls the take_image function to try to take images from all
		# 4 cameras but also blinks the blue indicator LED
		if time.time() > prev_capture_time + time_interval: # Note that if time_interval = inf, this if statement will never run, preventing any images from being taken.
			GPIO.output(led_pin,True) # Blink indicator LED to demonstrate status
			downlink.put(['CA','IM',take_image()]) # Call take image function and downlink output
			GPIO.output(led_pin,False)
			prev_capture_time = time.time() # Update prev_capture_time to prevent nonstop image capture
		time.sleep(1)
