import threading
import time 
import queue
from cama import cama
import dwlk
from moto import moto 
from sens import sens
 
tsens = threading.Thread(name='sens', target=sens.main)  
tdwlk = threading.Thread(name='dwlk', target=dwlk.main)
tmoto = threading.Thread(name='moto', target=moto.main)
tcama = threading.Thread(name='cama', target=cama.main)

print("about to give birth")
time.sleep(3)

print("birthing sens thread")
tsens.start()
print("sens thread birthed")
time.sleep(3)
print("birthing dwlk thread")
tdwlk.start()
print("dwlk thread birthed")
time.sleep(3)
print("birthing motor thread")
tmoto.start()
time.sleep(3)
print("moto thread birthed")
print("birthing camera thread")
tcama.start()
print("cama thread birthed")
print("Main Completed")
