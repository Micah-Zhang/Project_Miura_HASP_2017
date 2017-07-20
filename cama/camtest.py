import os
import time

timer = time.time()
os.system('fswebcam -d /dev/video0 -r 3264x2448 image0.jpg')
os.system('fswebcam -d /dev/video1 -r 3264x2448 image1.jpg')
os.system('fswebcam -d /dev/video2 -r 3264x2448 image2.jpg')
os.system('fswebcam -d /dev/video3 -r 3264x2448 image3.jpg')
timer = time.time() - timer
print(timer)

