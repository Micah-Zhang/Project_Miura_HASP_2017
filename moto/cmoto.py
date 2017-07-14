#motor and button variable init
Direction_Pin = 15
Step_Pin = 13
Upper_Button = 32
Lower_Button = 36
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
##motor setup
#GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)
##button setup
#GPIO.setup(Upper_Button,GPIO.IN)
#GPIO.setup(Lower_Button,GPIO.IN)

#flags
top_calib = False #initialize motor as uncalibrated
bot_calib = False #initialize motor as uncalibrated
step_count = 0 #tracks current stepcount
max_step = 17500 #tracks maxmimum stepcount
nudge_step = 0 #flag that keeps track of how many steps motor thread needs to nudge
nudge_state = False #flag that tells motor thread when it needs to nudge
current_percent = 0 #tracks percentage extension of payload at any time
minimum_success = False
full_extension = False
automation = False
wait_time = 1080 #wait 18 minutes between extension cycles
is_raised = False
cycle_start_time = 0 #keeps track of cycle start time
mission_start_time = 0
current_time = 0
