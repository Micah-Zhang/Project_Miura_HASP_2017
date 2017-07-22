import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(29,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)

GPIO.output(31,False)
GPIO.output(33,False)
GPIO.output(35,False)
GPIO.output(29,False)

GPIO.cleanup()
