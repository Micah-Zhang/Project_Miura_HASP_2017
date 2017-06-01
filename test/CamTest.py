import time
import picamera

camera = picamera.PiCamera()
try:
    camera.start_preview()
    time.sleep(10)
    camera.stop_preview()
finally:
    camera.close()

#INITIALIZE CAMERA
##camera = PiCamera()

###RESIZE PREVIEW WINDOW
##x = 0 #horizontal distance of preview window from upper left corner
##y = 530 #vertial ''
##width = 620 #width of preview window
##height = 480 #height ''
##
###DISPLAY CAMERA PREVIEW IN LOWER-LEFT CORNER WINDOW
##filename = '/home/pi/Desktop/image.jpg' #specify 
##camera.start_preview(fullscreen=False,window = (x,y,width,height))
##while(1):
##    ans = raw_input("Enter 'quit' to end preview. Enter 'pic' to take an image. Enter 'invert' to invert the preview. Enter 'crop' to impliment horizontal cropping: ")
##    if ans == "quit":
##        print("\nquitting \n")
##        break
##    elif ans == "pic":
##        print("\ntaking picture \n")
##        camera.capture(filename)
##        im = Image.open(filename)
##        im.show(im)
##    elif ans == "invert":
##        print("\ninverting\n")
##        camera.stop_preview() 
##        camera.vlip = False
##        camera.start_preview(fullscreen=False,window = (x,y,width,height))
##    elif ans == "crop":
##        camera.stop_preview() 
##        camera.crop = (0.0, 0.0, 0.5, 1.0)
##        camera.start_preview(fullscreen=False,window = (10,y,450,600))
##
###END PREVIEW    
##camera.stop_preview() 


#One image
#camera.start_preview()
#sleep(3)
#camera.capture('/home/pi/Desktop/image.jpg')
#camera.stop_peview()

#Resolution
#camera.resolution = (2593, 1944)
#camera.framerate = 15
#camera.start_prevew()

#sleep(5)
#camera.capture('/home/pi/Desktop/text.jpg')
#camera.stop_preview()

#import serial
#s = serial.Serial("/dev/ttyAMA0")
#s.write(open("target.txt","rb").read())

