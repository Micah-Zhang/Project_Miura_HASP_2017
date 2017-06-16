import threading
import queue

# Import code for threading. All flight code must be initialized from the main function in the thread file
from sens import sens
from dwlk import dwlk
from uplk import uplk
from moto import motorthread
#from cama import cama ### REMOVE COMMENTS IT MOTORTHREAD FAILS
#from moto import INmoto
#from moto import OUTmoto

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
dwlk_args = (downlink,)
uplk_args = (downlink, run_exp, moto_cmd,)
sens_args = (downlink,)
moto_args = (run_exp, moto_cmd,) ###comment out if using OUTmoto and INmoto
#cama_args = (run_exp,) ### remove comments if using OUTmoto and INmoto
#OUTmoto_args = (run_exp,)
#INmoto_args = (run_exp,)

# Create thread objects
threads = [
	threading.Thread(name='uplk', target=uplk.main, args=uplk_args),
	threading.Thread(name='sens', target=sens.main, args=sens_args),
	threading.Thread(name='dwlk', target=dwlk.main, args=dwlk_args),
	threading.Thread(name='moto', target=motorthread.main, args=moto_args)
	###ADD COMMA TO END OF PREVIOUS LINE BEFORE COMMENTING OUT THE BELOW
	#thread.Thread(name='cama', target=cama.main, args=cama_args), ###creates new threads in case motorthread fails
	#thread.Thread(name='OUTmoto', target=OUTmoto.main, args=OUTmoto_args),
	#thread.Thread(name='INmoto', target=INmoto.py, args=INmoto_args)
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
