
import cv2
import time

def main():
	#initilize four cameras
	cam1 = cv2.VideoCapture(0)
	cam2 = cv2.VideoCapture(1)
	cam3 = cv2.VideoCapture(2)
	cam4 = cv2.VideoCapture(3)

	'''
	cam1.set(3, 3456.)
	cam1.set(4, 2304.)
	cam2.set(3, 3456.)
	cam2.set(4, 2304.)
	cam3.set(3, 3456.)
	cam3.set(4, 2304.)
	cam4.set(3, 3456.)
	cam4.set(4, 2304.)
	'''

	r0, frame1 = cam1.read()
	print("1 ", r0)
	r1, frame2 = cam2.read()
	print("2 ", r1)
	r2, frame3 = cam3.read()
	print("3 ", r2)
	r3, frame4 = cam4.read()
	print("4 ", r3)

	cv2.imwrite('/home/pi/7.19.17_test_images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cv2.imwrite('/home/pi/7.19.17_test_images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cv2.imwrite('/home/pi/7.19.17_test_images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cv2.imwrite('/home/pi/7.19.17_test_images/cam3/{:.0f}.jpg'.format(time.time()), frame4)

if __name__ == '__main__':
	main()

