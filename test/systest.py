# Motor Data Collection
# Collects step count, encoder data, and button presses
# Written: Dawson Beatty 7/5/17


import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Encoder:
	def __init__(self, pin_A, pin_B): # constructor
		self.pin_A = pin_A #what is pinA?
		self.pin_B = pin_B #what is pinB?

		self.encoder_count = 0 #self is needed to create variables that can be accessed by any function inside the class 

		self.pin_A_last_state = GPIO.input(self.pin_A)

		return # all python functions require manual returns. else it gets hung.

	def process_pulse(self):
		pin_A_state = GPIO.input(self.pin_A) # reads state of pinA
		# If states are different, that means a pulse has occured # what is a pulse?
		if self.pin_A_last_state != pin_A_state:
			# If the output of B is different to output of A, that means encoder is going down
			if GPIO.input(self.pin_B) == pin_A_state: 
				self.encoder_count += 1
			else:
				self.encoder_count -= 1
			print(self.encoder_count)
		self.pin_A_last_state = pin_A_state # keep track of current state for future comparisions

		return

	def check_encoder_count(self):
		return self.encoder_count

#def move(Direction_Pin,state):
#	if
#	GPIO.output(Direction_Pin,

# INITIALIZATION

pin_A = 18
pin_B = 16

Direction_Pin = 15
Step_Pin = 13

Upper_Button = 32
Lower_Button = 36

GPIO.setup(pin_A, GPIO.IN) # initialize pinA and pinB to be read by RPi.gpio
GPIO.setup(pin_B, GPIO.IN)

GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Upper_Button, GPIO.IN)
GPIO.setup(Lower_Button, GPIO.IN)

step = 0

encoder = Encoder(pin_A, pin_B) # create instance of encoder class

# END INITIALIZATION

# Go all the way down to start at consistent position
GPIO.output(Direction_Pin, GPIO.LOW)
while not GPIO.input(Lower_Button):
	GPIO.output(Step_Pin, GPIO.HIGH)
	GPIO.output(Step_Pin, GPIO.LOW)
	time.sleep(.0036)

# x2 min success
lines = []
for i in range(2):
	# move up to ~72% with step count
	GPIO.output(Direction_Pin, GPIO.HIGH)
	for steps in range (11600):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(STep_Pin, GPIO.LOW)
		step += 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} {} {} '.format(time.time(), step, encoder.check_encoder_count(), GPIO.input(Upper_Button), GPIO.inp$
	with open('motor_data.txt','a') as f:
		for line in lines: # lines is an array of characters. this for loop iterates through the array, adding each character in the a$
			f.write(line+'\n')
	lines = []

	#time.sleep(100)

	#move down to 0% with button
	GPIO.output(Direction_Pin, GPIO.LOW) # change direction of motor
	while not GPIO.input(Lower_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		step += 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} {} {} '.format(time.time(), step, encoder.check_encoder_count(), GPIO.input(Upper_Button), GPIO.out$
	with open('motor_data.txt','a') as f:
		for line in lines: # lines is an array of characters. this for loop iterates through the array, adding each character in the a$
			f.write(line+'\n')
	lines = []

# x4 full ext
for i in range(4):
	# move up 100% with buttons
	GPIO.output(Direction_Pin, GPIO.HIGH) # Direction Pin = HIGH means go up
	while not GPIO.input(Upper_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		step += 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} {} {} '.format(time.time(), step, encoder.check_encoder_count(), GPIO.input(Upper_Button), GPIO.input(Lower_Button))) # where does the .append come from? what does it do?
	with open('motor_data.txt','a') as f:
		for line in lines: # lines is an array of characters. this for loop iterates through the array, adding each character in the a$
		f.write(line+'\n')
	lines = []

	#time.sleep(60)

	# move down 100% with buttons
	GPIO.output(Direction_Pin, GPIO.LOW) # change direction of motor
	while not GPIO.input(Lower_Button):
		GPIO.output(Step_Pin, GPIO.HIGH)
		GPIO.output(Step_Pin, GPIO.LOW)
		step += 1
		time.sleep(.0036)
		encoder.process_pulse()
		lines.append('{:.2f} {} {} {} {} '.format(time.time(), step, encoder.check_encoder_count(), GPIO.input(Upper_Button), GPIO.output(Lower_Button)))
	with open('motor_data.txt','a') as f:
		for line in lines: # lines is an array of characters. this for loop iterates through the array, adding each character in the a$
		f.write(line+'\n')
	lines = []


