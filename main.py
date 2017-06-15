import threading
import time
import queue
from cama import cama
#from moto import OUTmoto 
#from moto import moto
from sens import sens
from dwlk import dwlk
from uplk import uplk

q = queue.Queue()

tuplk = threading.Thread(name='uplk', target=uplk.main)
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
#tmoto = threading.Thread(name='moto', target=OUTmoto.main)
#tcama = threading.Thread(name='cama', target=cama.main)

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
