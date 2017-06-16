import time
import picamera
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import os
import datetime

'''
def capture(cam)
	timestamp = time.time()
	cmd = "raspistill -o capture_%d.jpg" % cam+timestamp
	os.system(cmd)
'''

def main(run_exp):
	if(run_exp.is_set()):
		#camera code with one camera directly connected to pi camera module
		count = 1
		time = 15
		cycle = 0
		switcher = 1
		with picamera.PiCamera() as camera:
			while True:
				cycle += 1
				count += 1
				#camera.start_preview()
				camera.resolution = (1024,768)
				camera.capture('image_{:d}.jpg'.format('Cycle_'+cycle+'_'+count))
				print("Picture taken")
				#camera.stop_preview()
				#cmd = "raspistill -o capture_{:d}.jpg".format(cam)
				time.sleep(time)
				switcher += 1
				if switcher == 4:
					time = 20
				elif switcher == 5:
					time = 115
				elif switcher == 6:
					time = 120
				elif switcher == 13:
					time = 15
				elif switcher == 17:
					time = 20
				elif switcher == 18:
					time = 595
				elif switcher == 19:
					switcher = 1
					cycle = 0
					time = 15
		
	#camera code for multiplexer with four cameras
	'''
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(12, GPIO.OUT)
	
	#camera A
	GPIO.output(7, False)
	GPIO.output(11, False)
	GPIO.output(12, True)
	capture('C1_')
	#cameraB
	GPIO.output(7, True)
        GPIO.output(11, False)
        GPIO.output(12, True)
 	capture('C2_')
	#cameraC
	GPIO.output(7, False)
        GPIO.output(11, True)
        GPIO.output(12, False)
	capture('C3_')
	#cameraD
	GPIO.output(7, True)
        GPIO.output(11, True)
        GPIO.output(12, False)
	capture('C4_')
	'''
