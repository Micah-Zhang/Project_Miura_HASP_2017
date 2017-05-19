import RPi.GPIO as GPIO #Import GPIO Library import time
import time

#blinking function
def blink(pin):
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(pin,GPIO.LOW)
	time.sleep(1)
	return

#to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

#set up GPIO output chennel
GPIO.setup(37, GPIO.OUT)

# blink GPI026 50 times
for i in range(0,50):
	blink(37)
	print("I luv potato")

#cleanup
GPIO.cleanup()

