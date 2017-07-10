import sens.fsens as fsens

# Sets sampling frequency for all sensors (in seconds)
TEMP_INTERVAL = 10
PRES_INTERVAL = 10
HUMI_INTERVAL = 10
ACCE_INTERVAL = 10


def main(downlink):

	scheduler = fsens.PeriodicScheduler() # Create a scheduler object that accesses the sensors file
	scheduler.setup(TEMP_INTERVAL, fsens.read_temp, downlink) # Set up temp sensors for scheduling, passing necessary argument 
	scheduler.setup(PRES_INTERVAL, fsens.read_pres, downlink) # Set up pressure sensors for scheduling, passing necessary arguments
	scheduler.setup(HUMI_INTERVAL, fsens.read_humi, downlink) # Set up humidity sensor for scheduling, passing necessary arguments
	scheduler.setup(ACCE_INTERVAL, fsens.read_acce, downlink) # Set up accelerometer for scheduling, passing necessary arguments

	scheduler.run() # Begin scheduling all sensors
	downlink.put(["SE", "BU", "SENS"]) # Verify that sensor thread started properly
