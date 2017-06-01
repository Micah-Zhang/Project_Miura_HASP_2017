import time
import RPi.GPIO as GPIO

Direction_Pin = 15
Step_Pin = 13

#initialize the motor
GPIO.setmode(GPIO.BOARD)

GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)

#ask for user input
direction = input("Would you like to move up or down, please enter up")

#tell motor to move either up or down
#UP = GPIO.HIGH, Down = GPIO.LOW

if direction == "up":
        GPIO.output(Direction_Pin, GPIO.HIGH)
elif direction == "down":
        GPIO.output(Direction_Pin, GPIO.LOW)
else:
        print("enter up or down please")

#tell motor to move XX number of steps
#ask for user input

steps = int(input("How many steps would you like to move?"))

for i in range(0, steps):
        GPIO.output(Step_Pin, GPIO.HIGH)
        GPIO.output(Step_Pin, GPIO.LOW)
        time.sleep(.02) #delay


#camera stuff

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)



GPIO.setup(7, GPIO.OUT)

GPIO.setup(11, GPIO.OUT)

GPIO.setup(12, GPIO.OUT)

def main():

        GPIO.output(7, True)

        GPIO.output(11, False)

        GPIO.output(12, True)

        capture(2)


def capture(cam):

        cmd = "raspistill -o capture_{:d}.jpg".format(cam)

        os.system(cmd)


if (__name__ == "__main__"):

        main()

        GPIO.output(7, False)

        GPIO.output(11, False)

        GPIO.output(12, True)




