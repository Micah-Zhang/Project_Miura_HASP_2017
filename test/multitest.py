import RPi.GPIO as gp
import os
from picamera import PiCamera
from time import sleep




gp.setwarnings(False)

gp.setmode(gp.BOARD)



gp.setup(7, gp.OUT)

gp.setup(11, gp.OUT)

gp.setup(12, gp.OUT)


def main():

	gp.output(7, True)
	gp.output(11, True)
	gp.output(12, False)

	a = 1
	while True:
		capture(a)
		a += 1
	
def capture(cam):

	'''
	camera = PiCamera()
	camera.start_preview()
	sleep(cam)
	camera.stop_preview()

	'''

	cmd = "raspistill -o capture_{:d}.jpg".format(cam)

	os.system(cmd)


if (__name__ == "__main__"):

	main()

	gp.output(7, False)

	gp.output(11, False)

	gp.output(12, True)



