'''
   ____  ____  ____      ____________________   __  _________  ______  ___ 
   / __ \/ __ \/ __ \    / / ____/ ____/_  __/  /  |/  /  _/ / / / __ \/   |
  / /_/ / /_/ / / / /_  / / __/ / /     / /    / /|_/ // // / / / /_/ / /| |
 / ____/ _, _/ /_/ / /_/ / /___/ /___  / /    / /  / // // /_/ / _, _/ ___ |
/_/   /_/ |_|\____/\____/_____/\____/ /_/    /_/  /_/___/\____/_/ |_/_/  |_|
    __  _____   _____ ____     ___   ____ ________            ___   ____ _______ 
   / / / /   | / ___// __ \   |__ \ / __ <  /__  /           |__ \ / __ <  ( __ )
  / /_/ / /| | \__ \/ /_/ /   __/ // / / / /  / /  ______    __/ // / / / / __  |
 / __  / ___ |___/ / ____/   / __// /_/ / /  / /  /_____/   / __// /_/ / / /_/ / 
/_/ /_/_/  |_/____/_/       /____/\____/_/  /_/            /____/\____/_/\____/  
'''

import sens.fsens as fsens

# Sets sampling frequency for all sensors (in seconds)
TEMP_INTERVAL = 1
HRBT_INTERVAL = 1
PRES_INTERVAL = 1
HUMI_INTERVAL = 1

def main(downlink, temp_led):#downlink
	downlink.put(["SE", "BU", "SENS"]) # Verify that sensor thread started properly
	scheduler = fsens.PeriodicScheduler() # Create a scheduler object that accesses the sensors file 
	scheduler.setup(TEMP_INTERVAL, fsens.read_temp,[downlink, temp_led])
	scheduler.setup(HRBT_INTERVAL, fsens.read_hrbt,[downlink]) # read heartbeat
	scheduler.setup(PRES_INTERVAL, fsens.read_pres,[downlink]) # Set up pressure sensors for scheduling, passing necessary arguments
	scheduler.setup(HUMI_INTERVAL, fsens.read_humi,[downlink]) # Set up humidity sensor for scheduling, passing necessary arguments
	scheduler.run() # Begin scheduling all sensors
