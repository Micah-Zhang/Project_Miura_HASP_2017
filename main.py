import threading
import time 
import queue
from camera import camera
import TESTdwlk
from motor import MImotor
from sensors import SENSORINTbby

q = queue.Queue()

t1  = threading.Thread(name='came', target=camera.main)
t2 =  threading.Thread(name='dwlk', target=TESTdwlk.main) 
t3  = threading.Thread(name='moto', target=MImotor.main)
t4 = threading.Thread(name='sens', target=SENSORINTbby.main)  

t4.start()
time.sleep(300)
t2.start()
t3.start()
t4.start()

print("Main Completed")
