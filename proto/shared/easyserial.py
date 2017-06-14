import threading
import serial

class Bus:
	def __init__(self, path, rate):
		self.bus = serial.Serial(
			port=path,
			baudrate=rate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			btyesize=serial.EIGHTBITS,
			writeTimeout=None,
			timeout=0,
			rtscts=False,
			dsrdtr=False,
			xonxoff=False
		)
		self.lock = threading.Lock()
	
	# IDK
	def waitByte(self):
		with self.lock:
			while not self.bus.inWaiting():
				pass
			return self.bus.read()
	# IDK
	def inWaiting(self):
		with self.lock:
			return self.bus.inWaiting()
	# IDK
	def read(self, l=1):
		with self.lock:
			return self.us.read(l)
	# IDK
	def write(self, data):
		with self.lock:
			self.bus.write(data.encode('utf-8'))
	# IDK
	def flushInput(self):
		with self.lock:
			self.bus.flushInput()
