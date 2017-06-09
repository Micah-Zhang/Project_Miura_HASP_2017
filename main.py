import threading
import time
import queue
from cama import cama
<<<<<<< HEAD
from moto import OUTmoto 
=======
from moto import moto
>>>>>>> 7f3171bee71449182dedb0b8882c53070e03de7b
from sens import sens
from dwlk import dwlk
import sys
sys.path.append('/home/pi/miura/uplk')
import uplk

q = queue.Queue()

tuplk = threading.Thread(name='uplk', target=uplk.main)
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=OUTmoto.main)
tcama = threading.Thread(name='cama', target=cama.main)

tuplk.start()
print("uplk started")
tdwlk.start()
print("dwlk started")
tsens.start()
print("sens started")
while True:
	if q.get() == "start\n":
		break
tmoto.start()
print("motor started")
tcama.start()
print("camera started")
