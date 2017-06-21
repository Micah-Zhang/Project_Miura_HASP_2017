################################################################################
#
# Title: MultiplexerPi Camera Test Program
#
#
#
#
#
#
#
################################################################################

import RPi.GPIO as gp
import os
import time
from picamera import PiCamera

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, False)
gp.output(15, True)
gp.output(16, True)
gp.output(21, False)
gp.output(22, True)


def main():

        answer = input("Hey pal, pick a camera please!: ")

        if answer == 'A':
                gp.output(7, False)
                gp.output(11, False)
                gp.output(12, True)
                time.sleep(2)
                capture(1) # Camera A
                time.sleep(5)

        if answer == 'B':
                gp.output(7, True)
                gp.output(11, False)
                gp.output(12, True)
                time.sleep(2)
                capture(2) # Camera B
                time.sleep(5)

        if answer == 'C':
                gp.output(7, False)
                gp.output(11, True)
                gp.output(12, False)
                time.sleep(2)
                capture(3) # Camera C
                time.sleep(5)

        if answer == 'D':
                print("Sorry! That camera is broken :/")
                '''
                gp.output(7, False)
                gp.output(11, True)
                gp.output(12, False)
                time.sleep(2)
                capture(3) # Camera C
                time.sleep(5)
                '''

        # catch all
        #if answer != "A" & answer != "B" & answer != "C" & answer != "D":
        #return

def capture(cam):

        cmd = "raspistill -o capture_%d.jpg" % cam
        os.system(cmd)
		
if __name__ == "__main__":

        # Run the program in a while loop that askes the user after each iteration
        # if they still want to run the program.

        Loop = 'y'

        while Loop == 'y':
                main()
                Loop = input("Hey buddy, would you like to run the program again friend? y/n: ")
        

        '''
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
        '''
            
