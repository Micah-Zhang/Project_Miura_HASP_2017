import RPi.GPIO as gp
import os
import time
from picamera import PiCamera

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

def main():

    camera = PiCamera()
    
    time.sleep(1)
    gp.output(7, True)
    gp.output(11, False)
    gp.output(12, True)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/miura/Camera/cameraBtest.jpg')
    camera.stop_preview()
    '''
    gp.output(7, True)
    gp.output(11, True)
    gp.output(12, False)
    time.sleep(5)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/miura/cama/cameraGtest.jpg')
    camera.stop_preview()
    
    
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    time.sleep(.1)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/miura/Camera/cameraAtest.jpg')
    camera.stop_preview()
    
    
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    camera.resolution = (1024, 768)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/pi/miura/cama/cameraCtest.jpg')
    camera.stop_preview()
    '''

    
if __name__ == "__main__":
    main()
    '''
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    '''
