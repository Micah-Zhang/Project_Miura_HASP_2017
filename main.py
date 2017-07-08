import threading
import queue

# Import code for threading. All flight code must be initialized from the main function in the thread file
from sens import sens
from dwlk import dwlk
from uplk import uplk
from moto import moto

# Import code shared between threads
from shared import easyserial

def shutdown():
	''' Completes all necessary events for a shutdown '''
	exit()

## Remove before flight pin: Check if the inhibit is active and set flag if it is 
#inhibit = 12
#gpio.setup(inhibit, gpio.IN)
#motorInhibit = True if gpio.input(inhibit) else False

# Create required Queues
moto_cmd = queue.Queue()
downlink = queue.Queue()

# Create shared objects
gnd_bus = easyserial.Bus("/dev/serial0", 4800)

# Setting up events to be seen across threads
# Event is like global boolean but safer for multithreading
run_exp = threading.Event() # Checks whether start command has been set

# Package arg tuples for thread
dwlk_args = (downlink, gnd_bus)
uplk_args = (downlink, gnd_bus, moto_cmd, run_exp)
sens_args = (downlink)
moto_args = (moto_cmd, run_exp)

# Create thread objects
threads = [
	threading.Thread(name='uplk', target=uplk.main, args=uplk_args),
	threading.Thread(name='sens', target=sens.main, args=sens_args),
	threading.Thread(name='dwlk', target=dwlk.main, args=dwlk_args),
	threading.Thread(name='moto', target=moto.main, args=moto_args)
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
