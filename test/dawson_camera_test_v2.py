import pygame.camera as pycam
import pygame.image as pyimg
import time

pycam.init()


class Camera:
	def __init__(self, camera_number):
		self.address = '/dev/video{}'.format(camera_number)
		self.image_folder = '/home/pi/miura/images/cam{}'.format(camera_number)
		
		self.cam = pycam.Camera(self.address,(64,48))

		self.initialized = False
		self.initialize()

	def initialize(self):
		for i in range(10):
			try:
				self.cam.start()
				print('Initialized')
				self.initialized = True
				return
				# Downlink success message
			except SystemError:
				time.sleep(1)
				pass

		# Downlink failure message. Could not initialize camera
		return 

	def take_image(self):
		if not self.initialized:
			return
		
		img = self.cam.get_image()
		pyimg.save(img, '{}/{:.0f}.png'.format(self.image_folder, time.time()))
		
		#TODO Add messages for success/failure. Check for existence of image? Check if size < 3.7MB? 
		# If image is properly saved as png, size will be compressed

		return
		
cameras = [Camera(i) for i in range(4)]

for camera in cameras:
	time.sleep(1)
	camera.take_image()

pycam.quit()

#import pygame.camera
#pygame.camera.init()
#cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
#cam.start()
#img = cam.get_image()
#import pygame.image
#pygame.image.save(img, "photo.bmp")
#pygame.camera.quit()
