import threading
import time 
import queue
from cama import cama
from moto import moto 
from sens import sens
import dwlk
 
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=moto.main)
tcama = threading.Thread(name='cama', target=cama.main)

tsens.start()
tdwlk.start()
time.sleep(300)
tmoto.start()
tcama.start()
