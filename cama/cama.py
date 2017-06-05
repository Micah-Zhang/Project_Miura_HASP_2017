import time
import picamera

def main():
	count = 1
	print("camera thread initiated")
	with picamera.PiCamera() as camera:
		while True:
			camera.resolution = (1024, 768)
			#camera.start_preview()
			# Camera warm-up time
			time.sleep(10)
			camera.capture('image_{:d}.jpg'.format(count))
			count += 1
			camera.stop_preview()
			#cmd = "raspistill -o capture_{:d}.jpg".format(cam)
