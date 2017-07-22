import sens.fsens as fsens

# Sets sampling frequency for all sensors (in seconds)
TEMP_INTERVAL = 1
HRBT_INTERVAL = 1
PRES_INTERVAL = 1
HUMI_INTERVAL = 1

def main(downlink):#downlink
	downlink.put(["SE", "BU", "SENS"]) # Verify that sensor thread started properly
	scheduler = fsens.PeriodicScheduler() # Create a scheduler object that accesses the sensors file 
	scheduler.setup(TEMP_INTERVAL, fsens.read_temp,[downlink])
	scheduler.setup(HRBT_INTERVAL, fsens.read_hrbt,[downlink]) # read heartbeat
	scheduler.setup(PRES_INTERVAL, fsens.read_pres,[downlink]) # Set up pressure sensors for scheduling, passing necessary arguments
	scheduler.setup(HUMI_INTERVAL, fsens.read_humi,[downlink]) # Set up humidity sensor for scheduling, passing necessary arguments
	scheduler.run() # Begin scheduling all sensors
