import cv2
import time

def take_images():
	# intiialize 4 cameras
	cam1 = cv2.VideoCapture(0)
	cam2 = cv2.VideoCapture(1)
	cam3 = cv2.VideoCaptrue(2)
	cam4 = cv2.VideoCapture(3)
	#take 4 images
	r0, frame1 = cam1.read()
	r1, frame2 = cam2.read()
	r2, frame3 = cam3.read()
	r3, frame4 = cam4.read()
	#save images appropriately
	cv2.imwrite('/home/pi/images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cv2.imwrite('/home/pi/images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cv2.imwrite('/home/pi/images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cv2.imwrite('/home/pi/images/cam3/{:.0f}.jpg'.format(time.time()), frame4)
