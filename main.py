import threading
import time
import queue
from cama import cama
from moto import moto
from sens import sens
from dwlk import dwlk
import sys
sys.path.append('/home/pi/miura/uplk')
import uplk

q = queue.Queue()

tuplk = threading.Thread(name='uplk', target=uplk.main)
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=moto.main)
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
