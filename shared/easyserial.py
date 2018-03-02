'''
    ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/
'''

import threading
import serial

class Bus:
	def __init__(self, path, rate): #constructor
		self.bus = serial.Serial( #not sure what self is
			port=path, #user input
			baudrate=rate, #user input
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			writeTimeout=None,
			timeout=0,
			rtscts=False, #IDK
			dsrdtr=False,
			xonxoff=False
		)
		self.lock = threading.Lock() #IDK

	def waitByte(self): #IDK
		with self.lock:
			while not self.bus.inWaiting():
				pass
			return self.bus.read()

	def inWaiting(self): #IDK
		with self.lock:
			return self.bus.inWaiting()

	def read(self, l=1): #read byte
		with self.lock:
			return self.bus.read(l)

	def write(self, data): #write byte
		with self.lock:
			self.bus.write(data.encode('utf-8'))

	def flushInput(self): #clears serial connection
		with self.lock:
			self.bus.flushInput()
