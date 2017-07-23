import cv2
import time

def main():
	print("taking image")
	cam1 = cv2.VideoCapture(0)
	cam1.set(3,1024.)
	cam1.set(4,768.)
	r0, frame1 = cam1.read()
	cv2.imwrite('/home/pi/images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cam1.release()
	
	print("1")
	
	cam2 = cv2.VideoCapture(1)
	cam2.set(3,1024.)
	cam2.set(4,768.)
	r1, frame2 = cam2.read()
	cv2.imwrite('/home/pi/images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cam2.release()	

	print("2")

	cam3 = cv2.VideoCapture(2)
	cam3.set(3,1024.)
	cam3.set(4,768.)
	r2, frame3 = cam3.read()
	cv2.imwrite('/home/pi/images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cam3.release()		

	print("3")

	cam4 = cv2.VideoCapture(3)
	cam4.set(3,1024.)
	cam4.set(4,768.)
	r3, frame4 = cam4.read()
	cv2.imwrite('/home/pi/images/cam3/{:.0f}.jpg'.format(time.time()), frame4)
	cam4.release()	

	print("4")

	print("done taking image")

	'''
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
	print("set resolution")
	#take 4 images
	r0, frame1 = cam1.read()
	print("1")
	r1, frame2 = cam2.read()
	print("2")
	r2, frame3 = cam3.read()
	print("3")
	r3, frame4 = cam4.read()
	print("4")
	#save images appropriately
	cv2.imwrite('/home/pi/images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cv2.imwrite('/home/pi/images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cv2.imwrite('/home/pi/images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cv2.imwrite('/home/pi/images/cam3/{:.0f}.jpg'.format(time.time()), frame4)
	#deinitialize 4 cameras
	cv2.VideoCapture.release()
	print("done taking image")
	'''

if __name__ == '__main__':
	main()
