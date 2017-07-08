# Camera testing code
# All cameras plugged into USB hub
# USB hub powered through AC cord

# 7/8 3PM
# Encountered issue with /dev/video0 failing with message "Failed to open /dev/video0: Device or resource busy"
# When command run again, returns "Failed to open /dev/video0: No such file or directory"
# After running /again/, camera takes image without issue

# Suggested solution: Camera initialization function. Run command on each camera every second until returns succesfully, then downlink success message


import subprocess
import time
import shlex

class Camera:
	def __init__(self, camera_number):
		self.address = '/dev/video{}'.format(camera_number)
		self.image_folder = '/home/pi/miura/images/cam{}'.format(camera_number)
		
		self.initialized = False
		self.initialize()
	
	def init_image_cmd(self):
		return 'v4l2-ctl -d {} --stream-mmap=3 --stream-count=1 --stream-to={}/init_{:.0f}.jpg'.format(self.address, self.image_folder, time.time())

	def image_cmd(self):
		return 'v4l2-ctl -d {} --stream-mmap=3 --stream-count=1 --stream-to={}/{:.0f}.jpg'.format(self.address, self.image_folder, time.time())

	def initialize(self):
		for i in range(10):
			return_code = subprocess.call(shlex.split(self.init_image_cmd()))
			if return_code == 0:
				# Downlink success
				self.initialized = True
				print('Success')
				return
			time.sleep(1)
		# Downlink failure message. Could not initialize camera
		return 

	def take_image(self):
		if not self.initialized:
			return
		return_code = subprocess.call(shlex.split(self.image_cmd()))
		
		if return_code == 0:
			pass
			# Downlink success message
		else:
			pass
			# Downlink failure message

		return


camera0 = Camera(0)
camera1 = Camera(1)
camera2 = Camera(2)
camera3 = Camera(3)

cameras = [camera0, camera1, camera2, camera3]

for camera in cameras:
	camera.take_image()


