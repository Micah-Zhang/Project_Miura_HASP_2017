import os
import time

start = time.time()
os.system('fswebcam -i 0 -d /dev/video0 -r 1024x768 -S 10 test1.jpg')
os.system('fswebcam -i 0 -d /dev/video1 -r 1024x768 -S 10 test2.jpg')
os.system('fswebcam -i 0 -d /dev/video2 -r 1024x768 -S 10 test3.jpg')
os.system('fswebcam -i 0 -d /dev/video3 -r 1024x768 -S 10 test4.jpg')

print(time.time()-start)
