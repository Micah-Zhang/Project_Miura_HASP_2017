#motor and button variable init
Direction_Pin = 15
Step_Pin = 13
Upper_Button = 32
Lower_Button = 36

#flags
top_calib = False #initialize motor as uncalibrated
bot_calib = False #initialize motor as uncalibrated
step_count = 0 #tracks current stepcount
max_step = 14450 #tracks maxmimum stepcount
nudge_step = 0 #flag that keeps track of how many steps motor thread needs to nudge
nudge_state = False #flag that tells motor thread when it needs to nudge
current_percent = 0 #tracks percentage extension of payload at any time
minimum_success = False
full_extension = False
automation = False
top_wait_time = 30 #change before flight
bot_wait_time = 30 
auto_wait = 300
tmp_time = 0
motor_start_time = 0
motor_end_time = 0
cycle_start_time = 0 #keeps track of cycle start time
cycle_end_time = 0
mission_start_time = 0
cycle_count = -2
cmd_sent = False
auto_set = False
prev_dwlk_time = 0
cycle_extended = False
cycle_contracted = False
