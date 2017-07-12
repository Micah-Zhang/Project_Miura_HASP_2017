# motor and button variable init
Direction_Pin = 15
Step_Pin = 13
Upper_Button = 32
Lower_Button = 36
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# motor setup
GPIO.setup(Direction_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Step_Pin, GPIO.OUT, initial=GPIO.LOW)
# button setup
GPIO.setup(Upper_Button,GPIO.IN)
GPIO.setup(Lower_Button,GPIO.IN)

# flags
top_calib = False #initialize motor as uncalibrated
bot_calib = False #initialize motor as uncalibrated
step_count = 0 #what is current step?
max_step = 0 #what is max step?
nudge_step = 0 #how much to nudge?
nudge_state = False #ready for nudging?
start_time = 0
current_time = 0
