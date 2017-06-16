import RPi.GPIO as gp
import os
from picamera import PiCamera
from time import sleep
'''
import RPi.GPIO as gp
02
import os
03
 
04
gp.setwarnings(False)
05
gp.setmode(gp.BOARD)
06
 
07
gp.setup(7, gp.OUT)
08
gp.setup(11, gp.OUT)
09
gp.setup(12, gp.OUT)
10
 
11
gp.setup(15, gp.OUT)
12
gp.setup(16, gp.OUT)
13
gp.setup(21, gp.OUT)
14
gp.setup(22, gp.OUT)
15
 
16
gp.output(11, True)
17
gp.output(12, True)
18
gp.output(15, True)
19
gp.output(16, True)
20
gp.output(21, True)
21
gp.output(22, True)
22
 
23
def main():
24
    gp.output(7, False)
25
    gp.output(11, False)
26
    gp.output(12, True)
27
    capture(1)
28
 
29
    gp.output(7, True)
30
    gp.output(11, False)
31
    gp.output(12, True)
32
    capture(2)
33
 
34
    gp.output(7, False)
35
    gp.output(11, True)
36
    gp.output(12, False)
37
    capture(3)
38
 
39
    gp.output(7, True)
40
    gp.output(11, True)
41
    gp.output(12, False)
42
    capture(4)
43
 
44
def capture(cam):
45
    cmd = "raspistill -o capture_%d.jpg" % cam
46
    os.system(cmd)
47
 
48
if __name__ == "__main__":
49
    main()
50
 
51
    gp.output(7, False)
52
    gp.output(11, False)
53
    gp.output(12, True)


'''

gp.setwarnings(False)

gp.setmode(gp.BOARD)



gp.setup(7, gp.OUT)

gp.setup(11, gp.OUT)

gp.setup(12, gp.OUT)


def main():

	gp.output(7, False)
	gp.output(11, False)
	gp.output(12, True)
	
	gp.output(7, False)
	gp.output(11, True)
	gp.output(12, False)
	a = 1
	while True:
		capture(a)
		a += 1
	
def capture(cam):

	'''
	camera = PiCamera()
	camera.start_preview()
	sleep(cam)
	camera.stop_preview()

	'''

	cmd = "raspistill -o capture_{:d}.jpg".format(cam)

	os.system(cmd)


if (__name__ == "__main__"):

	main()

	gp.output(7, False)

	gp.output(11, False)

	gp.output(12, True)



