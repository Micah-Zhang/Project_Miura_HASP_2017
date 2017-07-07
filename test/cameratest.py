import os
import time

pic = 0
while pic<4:
	time.sleep(5)
	print("Camera 1:")
	os.system('fswebcam -d /dev/video0 -r 1280x780 --save camera1_{}.jpg'.format(pic))
	time.sleep(5)
	print("Camera 2:")
	os.system('fswebcam -d /dev/video1 -r 1280x720 --save camera2_{}.jpg'.format(pic))
	time.sleep(5)
	print("Camera 3:")
	os.system('fswebcam -d /dev/video2 -r 1280x720 --save camera3_{}.jpg'.format(pic))
	time.sleep(5)
	print("Camera 4:")
	os.system('fswebcam -d /dev/video3 -r 1280x720 --save camera4_{}.jpg'.format(pic))	
	pic += 1
