import cv2
import time
import RPi.GPIO as GPIO

def main():
	print("taking image")
	#intiialize 4 cameras
	cam1 = cv2.VideoCapture(0)
	cam2 = cv2.VideoCapture(1)
	cam3 = cv2.VideoCapture(2)
	cam4 = cv2.VideoCapture(3)
	#set resolution
	cam1.set(3,3264.)
	cam1.set(4,2448.)
	cam2.set(3,3264.)
	cam2.set(4,2448.)
	cam3.set(3,3264.)
	cam3.set(4,2448.)
	cam4.set(3,3264.)
	cam4.set(4,2448.)
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
	print("done taking image")

if __name__ == '__main__':
	main()
