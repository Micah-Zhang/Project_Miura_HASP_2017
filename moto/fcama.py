import cv2
import time
import numpy as np
#from moto import cmoto
#from moto import moto
#from moto import fmoto
from moto import cama

def cam_setup():
	#initilize four cameras
	cam1 = cv2.VideoCapture('/dev/video0')
	cam2 = cv2.VideoCapture('/dev/video1')
	cam3 = cv2.VideoCapture('/dev/video2')
	cam4 = cv2.VideoCapture('/dev/video3')

	#not sure what these setting are lol
	cam1.set(3, 3456.)
	cam1.set(4, 2304.)
	cam2.set(3, 3456.)
	cam2.set(4, 2304.)
	cam3.set(3, 3456.)
	cam3.set(4, 2304.)
	cam4.set(3, 3456.)
	cam4.set(4, 2304.)

	r0, frame1 = cam1.read()
	r1, frame2 = cam2.read()
	r2, frame3 = cam3.read()
	r3, frame4 = cam4.read()


def take_image():
	cv2.imwrite('/home/pi/miura/images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cv2.imwrite('/home/pi/miura/images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cv2.imwrite('/home/pi/miura/images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cv2.imwrite('/home/pi/miura/images/cam3/{:.0f}.jpg'.format(time.time()), frame4)

