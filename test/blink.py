import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

LEDS = [29, 31, 33, 35] # G, B, Y, R

for LED in LEDS:
	GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

while True:
	for LED in LEDS:
		GPIO.output(LED, GPIO.HIGH)
		time.sleep(.5)
		GPIO.output(LED, GPIO.LOW)
