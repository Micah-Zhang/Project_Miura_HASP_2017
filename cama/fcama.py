import cv2
import time

def main():
	cam1 = cv2.VideoCapture(0)
	cam1.set(3,1024.)
	cam1.set(4,768.)
	cam1.set(cv2.cv.CV_CAP_PROP_EXPOSURE,-10)
	r0, frame1 = cam1.read()
	cv2.imwrite('/home/pi/images/cam0/{:.0f}.jpg'.format(time.time()), frame1)
	cam1.release()

	cam2 = cv2.VideoCapture(1)
	cam2.set(3,1024.)
	cam2.set(4,768.)
	cam2.set(cv2.cv.CV_CAP_PROP_EXPOSURE,-10)
	r1, frame2 = cam2.read()
	cv2.imwrite('/home/pi/images/cam1/{:.0f}.jpg'.format(time.time()), frame2)
	cam2.release()

	cam3 = cv2.VideoCapture(2)
	cam3.set(3,1024.)
	cam3.set(4,768.)
	cam3.set(cv2.cv.CV_CAP_PROP_EXPOSURE,-10)
	r2, frame3 = cam3.read()
	cv2.imwrite('/home/pi/images/cam2/{:.0f}.jpg'.format(time.time()), frame3)
	cam3.release()

	cam4 = cv2.VideoCapture(3)
	cam4.set(3,1024.)
	cam4.set(4,768.)
	cam4.set(cv2.cv.CV_CAP_PROP_EXPOSURE,-10)
	r3, frame4 = cam4.read()
	cv2.imwrite('/home/pi/images/cam3/{:.0f}.jpg'.format(time.time()), frame4)
	cam4.release()

	print map(int, [r0,r1,r2,r3])

if __name__ == '__main__':
	main()

'''
	print(cam1.get(CAP_PROP_BIRHG))
	print(cam1.get(CV_CAP_PROP_BRIGHTNESS))
	print(cam1.get(CV_CAP_PROP_CONTRAST))
	print(cam1.get(CV_CAP_PROP_SATURATION))
	print(cam1.get(CV_CAP_PROP_HUE))
	print(cam1.get(CV_CAP_PROP_GAIN))
	print(cam1.get(CV_CAP_PROP_EXPOSURE))
	print(cam1.get(CV_CAP_PROP_WHITE_BALANCE_U))
	print(cam1.get(CV_CAP_PROP_WHITE_BALANCE_V))
	print(cam1.get(CV_CAP_PROP_ISO_SPEED))
	print("\n")
'''
