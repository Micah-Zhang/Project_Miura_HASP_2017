import time
import picamera
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

def main():
	count = 1
	with picamera.PiCamera() as camera:
		while True:
			#camera.start_preview()
			camera.resolution = (1024,768)
			time.sleep(10)
			camera.capture('image_{:d}.jpg'.format(count))
			print("Picture taken")
			count += 1
			#camera.stop_preview()
			#cmd = "raspistill -o capture_{:d}.jpg".format(cam)
