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

#motor and button variable init
Direction_Pin = 15
Step_Pin = 13
Upper_Button = 32
Lower_Button = 36

# Note: many of these flags are logic "gates". For example, a full extension cycle consists of 4 parts: go up, wait for 18 minutes,
# go down, wait 10 minutes. To prevent all 4 parts from executing at once, these 4 parts are placed behind different conditionals.
# The flags are the "keys" to the gates. And depending on which flags are TRUE and which are FALSE, different parts of the full extension
# cycle execute.

#motor thread flags. DO NOT CHANGE. doing so will break the logic.
top_calib = False #initialize motor as uncalibrated
bot_calib = False #initialize motor as uncalibrated
step_count = 0 #tracks current stepcount
max_step = 16000 #tracks maxmimum stepcount
nudge_step = 0 #flag that keeps track of how many steps motor thread needs to nudge
nudge_state = False #flag that tells motor thread when it needs to nudge
minimum_success = False # Key for 1st part of min_success cycle
full_extension = False # Key for 1st part of full_extension cycle
automation = False # Flag must be true for automation process to occur
top_wait_time = 1080 #1080 = 18 minutes #change before flight
bot_wait_time = 600 #600 = 10 minutes #change before flight
auto_wait = 18000 #18000 = 5 hours #change before flight
motor_start_time = 0 # Key for 4th part of min_sucess and full_extension cycle
motor_end_time = 0 # Key for 4th part of min_sucess and full_extension cycle
cycle_start_time = 0 #keeps track of cycle start time
cycle_end_time = 0 #keeps track of cycle end time
mission_start_time = 0 #keeps track of mission start time
cycle_count = -2 # Tracks cycle count
cmd_sent = False # Key used in the automation "cycle"
auto_set = False # Prevents automation flag from being automatically set more than once
cycle_extended = False # Key for 2nd part of min_success and full_extension cycle
cycle_contracted = False # Key for 3rd part of min_success and full_extension cycle
