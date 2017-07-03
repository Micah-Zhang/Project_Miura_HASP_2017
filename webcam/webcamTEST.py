'''
import subprocess

subprocess.Popen(["fswebcam", "image.jpg"])

'''


'''
#!/bin/bash

fswebcam image1.jpg
'''

import os
import time

pic = 0

while pic<6:
    time.sleep(5)
    os.system('fswebcam -d /dev/video0 --save blackimage{}.jpg'.format(pic))
    pic += 1
    '''
    time.sleep(5)
    os.system('fswebcam -d /dev/video1 --save redimage{}.jpg'.format(pic))
    pic += 1
    '''
