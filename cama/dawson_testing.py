#import cv2
import time

import RPi.GPIO as GPIO

def image_function(index):
	cam = cv2.VideoCapture(index)
	cam.set(3, 3456.)
	cam.set(4, 2304.)

	ret, frame = cam.read()

	cv2.imwrite('/home/pi/miura/images/{:.0f}.jpg'.format(time.time()), frame)

	cam.release()
	return




for i in range(5):
	time.sleep(1)
	image_function(i)

