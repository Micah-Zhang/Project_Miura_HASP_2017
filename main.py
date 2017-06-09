import threading
import time 
import queue
from cama import cama
from moto import OUTmoto 
from sens import sens
from dwlk import dwlk
 
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=OUTmoto.main)
tcama = threading.Thread(name='cama', target=cama.main)

tsens.start()
tdwlk.start()
tmoto.start()
tcama.start()
