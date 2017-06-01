import threading
import time


# Print constantly 
def func_1():
    while True:
        time.sleep(.1)
        print('boop')
    

# Print statement after delay
def func_2():
    while True:
        time.sleep(2)
        print('Hello Micah')
        

thread_1 = threading.Thread(target=func_1)
thread_2 = threading.Thread(target=func_2)

#thread_1.start()
#thread_2.start()



















import sys
sys.exit()


class Micah:
    def __init__(self, speech):
        self.speech = speech
    
    def speak(self):
        return self.speech
        

CDH_Micah = Micah('Python is kewl') 

EPS_Micah = Micah('I do not fry sensors')

print('CDH Micah says ' + CDH_Micah.speak())
CDH_Micah.speech  = 'nevermind'
print('CDH Micah says ' + CDH_Micah.speak())

print('EPS Micah says ' + EPS_Micah.speak())
    
    
# self is a keyword which points to instance
class LED:
    def __init__(self, GPIO_pin):
        self.GPIO_pin = GPIO_pin
        
    def blink(self):
        pass       

# our_Micah is instance of Micah class        
#our_Micah = Micah() # Runs __init__()

# hair_color is an attribute of the instance 
#print(our_Micah.hair_color)

#our_Micah.speak() # Runs speak()

