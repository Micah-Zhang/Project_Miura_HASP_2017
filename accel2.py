#Original code at https://github.com/adafruit/Adafruit_Python_ADXL345/blob/master/examples/simpletest.py

import time
import adafruit_adxl345

accel = Adafruit_ADXL345.ADXL345()

print('Printing X,Y,Z axis values')
while True:
    x,y,z = accel.read()
    print('X = {0}, Y = {1}, Z = {2}'.format(x,y,z))
    time.sleep(1)
    
