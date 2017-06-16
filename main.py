import threading
import queue

# Import code for threading. All flight code must be initialized from the main function in the thread file
from sens import sens
from dwlk import dwlk
from uplk import uplk
from moto import motorthread

def shutdown():
	''' Completes all necessary events for a shutdown '''
	#camera.close()
	exit()

# Create required Queues
moto_cmd = queue.Queue()
downlink = queue.Queue()

# Setting up events to be seen across threads
# Event is like global boolean but safer for multithreading
run_exp = threading.Event()

# Package arg tuples for thread
dwlk_args = (downlink)
uplk_args = (downlink, run_exp, moto_cmd)
sens_args = (downlink)
moto_args = (downlink, run_exp, moto_cmd)

# Create thread objects
threads = [
	threading.Thread(name='uplk', target=uplk.main, args=uplk_args),
	threading.Thread(name='sens', target=sens.main, args=sens_args),
	threading.Thread(name='dwlk', target=dwlk.main, args=dwlk_args),
	threading.Thread(name='moto', target=motorthread.main, args=moto_args)
]

# Start running threads within a try-except block to allow for it to catch exceptions
try:
	for t in threads:
		t.daemon = True # Prevents it from running without main
		t.start()
	while True:
		for t in threads:
			t.join(3) # Prevent main from quitting by joining threads
except(KeyboardInterrupt, SystemExit):
	# Capture an exit condition and shut down the flight code
	shutdown()

'''
tuplk.start()
print("uplk started")
tdwlk.start()
print("dwlk started")
tsens.start()
print("sens started")
#tmoto.start()
#print("motor started")
#tcama.start()
#print("camera started")
'''
