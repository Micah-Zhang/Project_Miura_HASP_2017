import threading
import time 
import queue
from camera import TESTcam
from downlink import TESTdwlk
from motor import TESTmotor
from sensors import TESTsensor

q = queue.Queue()

t1  = threading.Thread(name='came', target=TESTcam.main)
t2 =  threading.Thread(name='dwlk', target=TESTdwlk.main) 
t3  = threading.Thread(name='moto', target=TESTmotor.main)
t4 = threading.Thread(name='sens', target=TESTsensor.main)  

t1.start()
t2.start()
t3.start()
t4.start()

#print(TESTcam.q.get())
#print(TESTdwlk.q.get())

print("Main Completed")
