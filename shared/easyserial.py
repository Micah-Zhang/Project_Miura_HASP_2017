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
