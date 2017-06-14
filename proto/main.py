import threading
import queue

# Set up GPIO pin for motor inhibit
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

def shutdown():
	""" Complete all necessary events for a shutdown """
	camera.close()
	exit()

# Import code for threading. All flight code must be initialized from the main function in the thread file
from cama import cama
from moto import moto
from sens import sens
from uplk import uplk
from dwlk import dwlk

# Directory for all code shared between threads
from shared import easyserial
