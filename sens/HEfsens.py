import sched
import time
import calendar

from w1thermsensor import W1ThermSensor


PRES_ADDR = 0x60

# Don't know what any of this is
AG_ADDR = 0x69
AG_POWER = 0x6b
AG_REG_AX = 0x3b
AG_REG_AY = 0x3d
AG_REG_AZ = 0x3f
AG_REG_GX = 0x43
AG_REG_GY = 0x45
AG_REG_GZ = 0x47

# No idea what this does.
temp_cal = [58.1723, 2.0657, 2.1016, 2.1210, 1.7322, 1.4072, 2.0503, 1.9183, 1.5197, 55.7113]
# Each value in list/tuple corresponds to the maximum value of a temp sensor
temp_max = [ 120.,  120.,  120.,  120.,  120.,  120.,  120.,  120.,  120., 120.,  120.,  120.,  120.,  120.]
# Above max is a place holder, can replace with actual values later


# What does the scheduler do?
class PeriodicScheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        self.scheduler.enter(interval, 1, self.setup, (interval, action, actionargs))
        action(*actionargs)

    def run(self):
        self.scheduler.run()


# Converts data array into string
def cs_str(data):
    out = "" # Initialize variable with empty string
    for i in range(len(data)): # Iterate through each "word" in data
        out += "%f " % (data[i]) # Add each word to the string "out"
   # out += "%f" % (data[-1])
    return out # Return newly formed string

'''
def capt(camera):
    t = calendar.timegm(time.gmtime()) # Grab GMT timestamp
    camera.save("/home/pi/miura/images/%i.png" % t) # Save image with timestamp as name
'''

def tempCheck(temps): # Check for overheating
    # Checks if any temperature readings are outside expected values
    tempBools = [tempI > maxI for tempI,maxI in zip(temps,temp_max)] # Compares each inputed temp values with its corresponding max temp and places booleans in a list
    # Returns true if one or more things is on fire. :(
    return any(tempBools) # If True appears anywhere in the list, return true. Otherwise, return false.


def temp(downlink, tempLED):
    try:
        data_raw = []
        data = []
        for sensor in W1ThermSensor.get_available_sensors(): # Grab temp values from all available sensors in a round robin fashion
            data_raw.append(sensor.get_temperature())
        for i in range(len(data_raw)): # Copy raw temp values into file meant for converted values. Was not fully implemented.
            data.append(data_raw[i])
            #data.append(temp_cal[i] + data_raw[i])
        if (not tempLED.is_set()) and tempCheck(data): # If any temp sensors are overheating and the temp LED is not on, turn it on.
            # If the flag isn't set, and things are on fire.
            tempLED.set()
        downlink.put(["SE", "T%i" % (len(data)), cs_str(data)]) # Send the packaged data packet to the downlink thread.
    except:
        print("Temperature reading failed")


def pres(downlink, bus):
    try:
        d = bus.read(PRES_ADDR, 2) # Read pressure sensor using i2c class
        data = int.from_bytes(d, byteorder='big', signed=False) # Convert bytes read into unsigned integers
        downlink.put(["SE", "PR", " %f" % (15 * data / 0x3FFF)]) # Package data for downlink using conversion factor
    except:
        pass

# Don't know what this is.
def ag_init(bus):
    bus.sm_write(AG_ADDR, AG_POWER, 0)

# Don't know what this is.
def ag(downlink, bus):
    try:
        time.sleep(0.05)
        data1 = bus.sm_read_word_2c(AG_ADDR, AG_REG_AX)
        data1 /= 16384.0
        data1 -= 0.0332
        time.sleep(0.05)
        data2 = bus.sm_read_word_2c(AG_ADDR, AG_REG_AY)
        data2 /= 16384.0
        data2 += 0.0635
        time.sleep(0.05)
        data3 = bus.sm_read_word_2c(AG_ADDR, AG_REG_AZ)
        data3 /= 16384.0
        data3 += 0.008
        time.sleep(0.05)
        data4 = bus.sm_read_word_2c(AG_ADDR, AG_REG_GX)
        data4 /= 131
        data4 -= 0.1608
        time.sleep(0.05)
        data5 = bus.sm_read_word_2c(AG_ADDR, AG_REG_GY)
        data5 /= 131 - 0.4527
        time.sleep(0.05)
        data6 = bus.sm_read_word_2c(AG_ADDR, AG_REG_GZ)
        data6 /= 131
        data6 -= 1.2578
        data = [data1, data2, data3, data4, data5, data6]
        downlink.put(["SE", "AG", cs_str(data)])
    except:
        pass
