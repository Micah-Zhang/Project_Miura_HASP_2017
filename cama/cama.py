import time
import picamera

def main():
	print("Taking picture")
	time.sleep(10)
	'''
	count = 1
	with picamera.PiCamera() as camera:
		while True:
			#camera.start_preview()
			camera.resolution = (1024,768)
			time.sleep(10)
			camera.capture('image_{:d}.jpg'.format(count))
			count += 1
			#camera.stop_preview()
			#cmd = "raspistill -o capture_{:d}.jpg".format(cam)
	'''
