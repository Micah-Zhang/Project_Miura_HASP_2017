import sens.fsens as fsens
#import fsens
#from fsens import *

# Sets sampling frequency for all sensors (in seconds)
TEMP_INTERVAL = 1
PRES_INTERVAL = 1
HUMI_INTERVAL = 1
ACCE_INTERVAL = 1


def main(downlink):#downlink
	downlink.put(["SE", "BU", "SENS"]) # Verify that sensor thread started properly
	scheduler = fsens.PeriodicScheduler() # Create a scheduler object that accesses the sensors file
	scheduler.setup(TEMP_INTERVAL, fsens.read_temp,[downlink]) # Set up temp sensors for scheduling, passing necessary argument 
	scheduler.setup(PRES_INTERVAL, fsens.read_pres,[downlink]) # Set up pressure sensors for scheduling, passing necessary arguments
	scheduler.setup(HUMI_INTERVAL, fsens.read_humi,[downlink]) # Set up humidity sensor for scheduling, passing necessary arguments
	scheduler.setup(ACCE_INTERVAL, fsens.read_acce,[downlink]) # Set up accelerometer for scheduling, passing necessary arguments
	
	scheduler.run() # Begin scheduling all sensors
