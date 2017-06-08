import threading
import time 
import queue
from cama import cama
from moto import moto 
from sens import sens
from dwlk import dwlk
from uplk import uplk
 
tuplk = threading.Thread(name='uplk', target=uplk.main)
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=moto.main)
tcama = threading.Thread(name='cama', target=cama.main)

tuplk.start()
tdwlk.start()
tsens.start()
tmoto.start()
tcama.start()
