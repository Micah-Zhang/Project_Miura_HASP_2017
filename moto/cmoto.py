#motor and button variable init
Direction_Pin = 15
Step_Pin = 13
Upper_Button = 32
Lower_Button = 36

#motor thread flags. DO NOT CHANGE. doing so will break the logic.
top_calib = False #initialize motor as uncalibrated
bot_calib = False #initialize motor as uncalibrated
step_count = 0 #tracks current stepcount
max_step = 16000 #tracks maxmimum stepcount
nudge_step = 0 #flag that keeps track of how many steps motor thread needs to nudge
nudge_state = False #flag that tells motor thread when it needs to nudge
minimum_success = False
full_extension = False
automation = False
top_wait_time = 1080 #1080 = 18 minutes #change before flight
bot_wait_time = 600 #600 = 10 minutes #change before flight
auto_wait = 18000 #18000 = 5 hours #change before flight
motor_start_time = 0
motor_end_time = 0
cycle_start_time = 0 #keeps track of cycle start time
cycle_end_time = 0
mission_start_time = 0
cycle_count = -2
cmd_sent = False
auto_set = False
cycle_extended = False
cycle_contracted = False
