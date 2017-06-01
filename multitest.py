import RPi.GPIO as gp
import os



gp.setwarnings(False)

gp.setmode(gp.BOARD)



gp.setup(7, gp.OUT)

gp.setup(11, gp.OUT)

gp.setup(12, gp.OUT)



def main():

	gp.output(7, True)

	gp.output(11, False)

	gp.output(12, True)
	
	while True:
		
		a = 1
		capture(a)
		a = a+1


def capture(cam):

	cmd = "raspistill -o capture_{:d}.jpg".format(cam)

	os.system(cmd)



if (__name__ == "__main__"):

	main()

	gp.output(7, False)

	gp.output(11, False)

	gp.output(12, True)



