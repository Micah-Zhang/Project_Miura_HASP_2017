
import subprocess
import time
import shlex

class Camera:
	def __init__(self,camera_number):
		self.address = '/dev/video{}'.format(camera_number)
		self.image_folder = '/home/pi/miura/test/images/cam{}'.format(camera_number)
		self.config_cmd = "v412-ctl -d {} --set-fmt-video=width=1600,height=1200,pixelformat='YUYV'".format(self.address)
		subprocess.call(shlex.split(self.config_cmd))
		self.initialize()
	
	def initialize(camera_number):
		for i in range(10):
			init_fail = subprocess.call(shlex.split(self.init_image_cmd()))
			if init_fail == 0:
				print('Camera {} Initialized'.format(camera_number))
				return
			time.sleep(1)
		
camera1 = Camera(0)
camera2 = Camera(1)
camera3 = Camera(2)
camera4 = Camera(3)

cameras = [camera1, camera2, camera3, camera4]

for camera in cameras:
	camera.__init__()
