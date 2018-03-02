'''
    ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/
'''

import threading
import queue

# Import code for threading. All flight code must be initialized from the main function in the thread file
from sens import sens
from dwlk import dwlk
from uplk import uplk
from moto import moto
from cama import cama

# Import code shared between threads
from shared import easyserial

def shutdown():
	''' Completes all necessary events for a shutdown '''
	exit()

# Create required Queues
moto_cmd = queue.Queue()
downlink = queue.Queue()

# Create shared objects
gnd_bus = easyserial.Bus("/dev/ttyUSB0", 4800)

# Setting up events to be seen across threads
# Event is like global boolean but safer for multithreading
safe_mode = threading.Event()
temp_led = threading.Event()

#Threading events for camera
cam_is_moving = threading.Event()
cam_is_open = threading.Event()
cam_reset = threading.Event()

# Package arg tuples for thread
dwlk_args = (downlink, gnd_bus)
uplk_args = (downlink, gnd_bus, moto_cmd, safe_mode)
sens_args = (downlink, temp_led)
moto_args = (downlink, moto_cmd, safe_mode, cam_is_moving, cam_is_open, cam_reset)
cama_args = (downlink, cam_is_moving, cam_is_open, cam_reset)

# Create thread objects
threads = [
	threading.Thread(name='uplk', target=uplk.main, args=uplk_args),
	threading.Thread(name='sens', target=sens.main, args=sens_args),
	threading.Thread(name='dwlk', target=dwlk.main, args=dwlk_args),
	threading.Thread(name='moto', target=moto.main, args=moto_args),
	threading.Thread(name='cama', target=cama.main, args=cama_args)
]

# Start running threads within a try-except block to allow for it to catch exceptions
try:
	for t in threads:
		t.daemon = True # Prevents it from running without main
		t.start()
	while True:
		for t in threads:
			t.join(4) # Prevent main from quitting by joining threads
except(KeyboardInterrupt, SystemExit):
	# Capture an exit condition and shut down the flight code
	shutdown()
