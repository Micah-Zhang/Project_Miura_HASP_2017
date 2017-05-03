from picamera import PiCamera
from time import sleep

camera = PiCamera()

#Video 10 sec
camera.start_preview()
sleep(60)
camera.stop_preview() 

#One image
#camera.start_preview()
#sleep(3)
#camera.capture('/home/pi/Desktop/image.jpg')
#camera.stop_preview()

#Resolution
#camera.resolution = (2593, 1944)
#camera.framerate = 15
#camera.start_preview()

#sleep(5)
#camera.capture('/home/pi/Desktop/text.jpg')
#camera.stop_preview()

#import serial
#s = serial.Serial("/dev/ttyAMA0")
#s.write(open("target.txt","rb").read())

