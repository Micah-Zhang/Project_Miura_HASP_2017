import sens.sensors as sensors

CAM_INTERVAL = 10  # seconds
TEMP_INTERVAL = 10
PRES_INTERVAL = 10
AG_INTERVAL = 10


def main(downlink, i2c, camera, tempLED):

	sensors.ag_init(i2c) # Initialize i2c sensors
	scheduler = sensors.PeriodicScheduler() # Create a scheduler object that accesses the sensors file
	scheduler.setup(AG_INTERVAL, sensors.ag, [downlink, i2c]) # Set up ag for scheduling, passing necessary arguments
	scheduler.setup(CAM_INTERVAL, sensors.capt, [camera]) # Set up cameras for scheduling, passing necessary arguments 
	scheduler.setup(TEMP_INTERVAL, sensors.temp, [downlink, tempLED]) # Set up temp sensors for scheduling, passing necessary arguments
	scheduler.setup(PRES_INTERVAL, sensors.pres, [downlink, i2c]) # Set up pressure sensor for scheduling, passing necessary arguments

	scheduler.run() # Begin scheduling all sensors
	downlink.put(["SE", "BU", "SENS"]) # Verify that sensor thread started properly
