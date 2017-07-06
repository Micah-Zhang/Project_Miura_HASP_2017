# Motor Data Collection
# Collects step count, encoder data, and button presses
# Written: Dawson Beatty 7/5/17


import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Encoder:
	def __init__(self, pin_A, pin_B):
		self.pin_A = pin_A
		self.pin_B = pin_B

		self.encoder_count = 0

		self.pin_A_last_state = GPIO.input(self.pin_A)

		return

	def process_pulse(self):
		pin_A_state = GPIO.input(self.pin_A)
		# If states are different, that means a pulse has occured
		if self.pin_A_last_state != pin_A_state:
			# If the output of B is different to output of A, that means encoder is going down
			if GPIO.input(self.pin_B) == pin_A_state: 
				self.encoder_count += 1
			else:
				self.encoder_count -= 1
			print(self.encoder_count)
		self.pin_A_last_state = pin_A_state

		return

	def check_encoder_count(self):
		return self.encoder_count



# INITIALIZATION

pin_A = 18
pin_B = 16

Direction_Pin = 15
Step_Pin = 13

Upper_Button = 32
Lower_Button = 36

GPIO.setup(pin_A, GPIO.IN)
GPIO.setup(pin_B, GPIO.IN)

GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Upper_Button, GPIO.IN)
GPIO.setup(Lower_Button, GPIO.IN)

step = 0

encoder = Encoder(pin_A, pin_B)

# END INITIALIZATION

# Go all the way down to start at consistent position
GPIO.output(Direction_Pin, GPIO.LOW)
while not GPIO.input(Lower_Button):
	GPIO.output(Step_Pin, GPIO.HIGH)
	GPIO.output(Step_Pin, GPIO.LOW)
	time.sleep(.0036)

lines = []

# Run cycles until operator gets bored
for i in range(10):
	GPIO.output(Direction_Pin, GPIO.HIGH)
	while not GPIO.input(Upper_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		step += 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} '.format(time.time(), step, encoder.check_encoder_count()))

	#time.sleep(60)

	lines.append('{:.2f} UPPER BUTTON HIT'.format(time.time()))
	GPIO.output(Direction_Pin, GPIO.LOW)
	while not GPIO.input(Lower_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		step = 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} '.format(time.time(), step, encoder.check_encoder_count()))
	lines.append('{:.2f} LOWER BUTTON HIT'.format(time.time()))

	#time.sleep(60)

	with open('motor_data.txt','a') as f:
		for line in lines:
			f.write(line+'\n')
	lines = []


