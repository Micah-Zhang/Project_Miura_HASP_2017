################################################################################
# Pi Cam Module w/ Wide Angle Lens Control Program
#
# Authored by: Adam Farmer, Author Here, Author Here
# Created on: 5/11/17
# Edited on: 5/11/17
#
# Purpose: To provide control of the Pi Cam module and it's basic optional
#          functions.
#
################################################################################

# IMPORT LIBRARIES
from picamera import PiCamera
from time import sleep
from PIL import Image
import datetime as dt

# INITIALIZE CAMERA
camera = PiCamera()

# RESIZE PREVIEW WINDOW
x = 0 #horizontal distance of preview window from upper left corner
y = 530 #vertial distance of preview window from upper left corner
width = 620 #width of preview window
height = 480 #height of preview window

# DISPLAY CAMERA PREVIEW IN LOWER-LEFT CORNER WINDOW
filename = '/home/pi/Desktop/image.jpg' #specify 
camera.start_preview(fullscreen=False,window = (x,y,width,height))
print("---------------------------------------------------------------")
print("\n   Welcome to the Wide Angle Pi Cam Module Control Program! \n")
print("---------------------------------------------------------------")

print("Enter 'quit' to end preview. \n")
print("Enter 'pic' to capture an image. \n")
print("Enter 'invert' to flip the preview along the vertical axis \n")
print("Enter 'crop' to implement horizontal cropping \n")
print("Type 'kill ' and then an optional command to undo that operation. \n")

while(1):

    # MAIN MENU OPTIONS AND INPUT PROMPT
    ans = raw_input("Please enter a command: ")
    print("\n Enter 'quit' to end preview. \n")
    print("Enter 'pic' to capture an image. \n")
    print("Enter 'invert' to flip the preview along the vertical axis \n")
    print("Enter 'crop' to implement horizontal cropping \n")
    print("Type 'kill ' and then an optional command to undo that operation. \n")

    # BASIC CAMERA OPERATIONS
    if ans == "quit":
        print("\n good bye! \n")
        break
    
    elif ans == "pic":
        print("\n capturing image \n")
        #time_var = time.strftime("%d%m%y")
        camera.annotate_text = dt.datetime.now().strftime('%y-%m-%d %H:%M:%S') #timestamp
        camera.capture(filename)
        im = Image.open(filename)
        im.show(im)
        camera.annotate_text = " " #kill annotate_text

    # CAMERA OPTIONS AN THIER 'KILL' COMMANDS
        
    # invert preview
    elif ans == "invert":
        print("\n inverting \n")
        camera.stop_preview() 
        camera.vlip = True
        camera.start_preview(fullscreen=False,window = (x,y,width,height))
    elif ans == "kill invert":
        print("\n killing inverting \n")
        camera.stop_preview() 
        camera.vlip = False
        camera.start_preview(fullscreen=False,window = (x,y,width,height))
        
    # implement horizontal cropping
    elif ans == "crop":
        print("\n cropping \n")
        camera.stop_preview() 
        camera.crop = (0.0, 0.0, 0.5, 1.0)
        camera.start_preview(fullscreen=False,window = (10,y,620,480))
    elif ans == "kill crop":
        print("\n killing cropping \n")
        camera.stop_preview() 
        camera.crop = (0.0, 0.0, 1.0, 1.0)
        camera.start_preview(fullscreen=False,window = (x,y,width,height))

# END PREVIEW    
camera.stop_preview() 
