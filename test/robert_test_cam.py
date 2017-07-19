import cv2
import time

cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(2)
cam3 = cv2.VideoCapture(3)


#cam1.set(3, 3456.)
#cam1.set(4, 2304.)


r0, frame0 = cam0.read()
print(r0)

r1, frame1 = cam1.read()
print(r1)

r2, frame2 = cam2.read()
print(r2)

r3, frame3 = cam3.read()
print(r2)

#cv2.imwrite('test0.jpg', frame0)
cv2.imwrite('test_im/cam0_{:.0f}.jpg'.format(time.time()) , frame0) 
cv2.imwrite('test_im/cam1_{:.0f}.jpg'.format(time.time()) , frame1) 
cv2.imwrite('test_im/cam2_{:.0f}.jpg'.format(time.time()) , frame2) 
cv2.imwrite('test_im/cam3_{:.0f}.jpg'.format(time.time()) , frame3) 

