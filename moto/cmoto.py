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
top_wait_time = 1080#change to 1080 for systems test
bot_wait_time = 600 #change to 600 for systems test
auto_wait = 300
is_raised = False
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
cycle_extending = False
cycle_contracting = False
image_request = False
