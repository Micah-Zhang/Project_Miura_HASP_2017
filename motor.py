
#*********************************************************#
#   COSGC Presents                                        #
#       _____  ____ __  ___ ____   ___                    #
#      / ___/ /  _//  |/  // __ ) /   |                   #
#      \__ \  / / / /|_/ // __  |/ /| |                   #
#     ___/ /_/ / / /  / // /_/ // ___ |                   #
#    /____//___//_/  /_//_____//_/  |_|                   #
#                                                         #
#  Copyright (c) 2015 University of Colorado Boulder      #
#  COSGC HASP SIMBA Team                                  #
#*********************************************************#

from __future__ import division # "/" operator does not floor result, to do integer division use "//"
import time
import logging
import queue
import threading
import RPi.GPIO as GPIO

DIR_PIN = 15 #pin to use for direction
STEP_PIN = 13 #pin to use for step
M0 = 29 #pin to use for M-naught for microstepping
M1 = 31 #pin to use for M-1 for microstepping
ENABLE_PIN = 11 #sleep pin for the motor
MICRO = 1.0/16 #microstep amount (1, 1/2, 1/4, 1/8, 1/16, 1/32)

MOTOR_MAX_HEIGHT = 10 #in cm

ASCENT_TIME = 60# 7200 #in seconds #2 hrs
FLOAT_TIME = 120#14400 #in seconds #4 hrs
RAISE_AUTOMATION_TIME = 60# 1800 #in seconds #30 min
LOWER_AUTOMATION_TIME = 60# 3600 #in seconds #1 hr
PRESSURE_EVALUATE_TIME = 60# 600 #in seconds #10 min

AUTOMATION_OVERRIDE = False
OVERRIDE_TIME = 0 #in seconds, will be updated by uplink
AUTOMATION_THRESHOLD = 1 #in bars

EXIT_MOTOR_AUTOMATION = False

#file to hold how far the motor has moved, in centimeters
MOTOR_STATUS_FILE = "/home/pi/miura/motor_status.txt"
       

#sets the sleep pin HIGH or LOW
def enable(enable=True):
    '''
    enables or disables the motor
    pass in True to enable or False to disable
    Pin number for ENABLE_PIN is in global variable above
    '''

    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    GPIO.output(ENABLE_PIN, enable)


#initializes the motor
def motor_init(micro=MICRO):
    '''
    Sets up the pins necessary to run the motor and initializes pins for microstepping
    Pin numbers for direction and step are in global variables above
    Pin numbers for M0 and M1 are in global variables above
    Different amounts to microstep are in global variable above
    NOTE!!! This does NOT set the enable pin to HIGH, the enable function must be called
    in addition to this function to actually run the motor
    '''

    #tells RPi.GPIO to use the BOARD numbering on the Pi (as opposed to BCM)
    GPIO.setmode(GPIO.BOARD)

    #set up the pins to output and initialize to LOW
    #initial=GPIO.LOW/GPIO.HIGH is an optional perameter
    GPIO.setup(DIR_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(STEP_PIN, GPIO.OUT, initial=GPIO.LOW)

    #for microstepping
    if micro == 1:
        GPIO.setup(M0, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(M1, GPIO.OUT, initial=GPIO.LOW)
    elif micro == 1/2:
        GPIO.setup(M0, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(M1, GPIO.OUT, initial=GPIO.LOW)
    elif micro == 1/4:
        #float M0, do nothing, pin will be floated as long as GPIO.cleanup() is run
        GPIO.setup(M1, GPIO.OUT, initial=GPIO.LOW)
    elif micro == 1/8:
        GPIO.setup(M0, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(M1, GPIO.OUT, initial=GPIO.HIGH)
    elif micro == 1/16:
        GPIO.setup(M0, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(M1, GPIO.OUT, initial=GPIO.HIGH)
    elif micro == 1/32:
        #float M0, do nothing, pin will be floated as long as GPIO.cleanup() is run
        GPIO.setup(M1, GPIO.OUT, initial=GPIO.HIGH)
    else:
        logging.error("microsteppng value invalid")

    #remember to run GPIO.cleanup() before changing microstep value
    #GPIO.cleanup() should be run at the end of a script using this function


#moves the MCU
def move(cm, direction, DOWNLINK_QUEUE, sleep=.002, step=False):
    '''
    Tells the motor to move a certain amount of linear centimeters (assumes not micro-stepping) in a certain direction
    Pass the method "up" to move up, or "down" to move down
    Pins for direction and step are in global variables above
    Microstepping amount in global variable above
    Can accept a different sleep value, which will speed up or slow down the stepping speed
        default is .002, which was tested to run quite smoothly
        not reccommended to go below .001, which is quite fast anyway
    If step is set to True, the passed in value (cm) will be the amount of steps to move, rather than cm to move
    Also opens the stored in motor_status_file and stores, in cm, the current location of the motor
    Takes DOWNLINK_QUEUE to send downlinks
    '''

    #for downlink
    centimeters = cm

    #calculate steps needed for microstepping
    cm *= (1 / MICRO)

    #depending on whether step is true or false
    if not step:
        #calculate amount of steps needed from centimeter value
        steps = cm/.004 #one step is 40um of linear movement
    else:
        #set steps to be passed in value
        steps = cm

    #floor steps and convert it to int, if it isn't already
    steps = int(steps)

    #set the DIR_PIN high or low, depending on the direction wanted to move
    #UP = GPIO.HIGH, DOWN = GPIO.LOW (depending on wiring)
    if direction == "up":
        GPIO.output(DIR_PIN, GPIO.HIGH)
    elif direction == "down":
        GPIO.output(DIR_PIN, GPIO.LOW)
    else:
        logging.error("direction invalid")

    #move desired amount of steps
    for i in range(0, steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(sleep) #delay

    #open status file and pull data
    motor_status_file = open(MOTOR_STATUS_FILE, "a+")
    lines = motor_status_file.readlines()
    status = float(lines[len(lines)-1])

    #downlink a confirmatin that movement is complete and write status to file
    if direction == "up":
        status += centimeters
        logging.warning("Finished moving up " + str(centimeters) + " cm")
        DOWNLINK_QUEUE.put(["MO", "MV", "UP" + str(centimeters)])
    elif direction == "down":
        #ensure status is never negative
        if status - centimeters <= 0:
            status = 0
        else:
            status -= centimeters
        logging.warning("Finished moving down " + str(centimeters) + " cm")
        DOWNLINK_QUEUE.put(["MO", "MV", "DOWN" + str(centimeters)])

    #write new data to status file
    motor_status_file.write(str(status))
    motor_status_file.write("\n")
    motor_status_file.close()

    #GPIO.cleanup() should be run at the end of a script using this function


#worker function for command_handler thread
def command_handler(DOWNLINK_QUEUE, COMMAND_HANDLER_QUEUE, MOTOR_QUEUE):
    '''
    this thread function waits for commands in COMMAND_HANDLER_QUEUE and executes them
    Takes DOWNLINK_QUEUE to downlink messages, COMMAND_HANDLER_QUEUE to search for commands
    and MOTOR_QUEUE to verify when the thread has died
    '''

    #thread initialization
    logging.info("Thread initialized")
    DOWNLINK_QUEUE.put(["CH", "BU", "COMM"])

    #global variables
    global AUTOMATION_OVERRIDE
    global OVERRIDE_TIME
    global EXIT_MOTOR_AUTOMATION

    #for exiting the thread
    loop_break = False

    while True:
        #search the queue
        while not COMMAND_HANDLER_QUEUE.empty():
            cmd = COMMAND_HANDLER_QUEUE.get()

            #auto raise, no longer used (I think)
            if cmd == "UP_AUTO":
                #downlink
                logging.warning("Raising the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "RS"])

                #move
                enable(True)
                move(MOTOR_MAX_HEIGHT, "up", DOWNLINK_QUEUE)
                enable(False)

            #auto lower, no longer used (I think)
            elif cmd == "DOWN_AUTO":
                #downlink
                logging.warning("Lowering the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "LOW"])

                #move
                enable(True)
                move(MOTOR_MAX_HEIGHT + .1, "down", DOWNLINK_QUEUE)
                enable(False)

            #move up the full amount, ends automation
            elif cmd == "UP":
                #downlink
                logging.warning("Raising the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "RS"])

                #end automation
                EXIT_MOTOR_AUTOMATION = True

                #move
                enable(True)
                move(MOTOR_MAX_HEIGHT, "up", DOWNLINK_QUEUE)
                enable(False)

            #move down the full amount, ends automation
            elif cmd == "DOWN":
                #downlink
                logging.warning("Lowering the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "LOW"])

                #end automation
                EXIT_MOTOR_AUTOMATION = True

                #move
                enable(True)
                move(MOTOR_MAX_HEIGHT + .1, "down", DOWNLINK_QUEUE)
                enable(False)

            #sets the enable pin to LOW
            elif cmd == "DISABLE_MCU":
                #downlink
                logging.warning("Disabling the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "DIS"])

                #disable
                enable(False)

            #sets the enable pin to HIGH
            elif cmd == "ENABLE_MCU":
                #downlink
                logging.warning("Enabling the MCU")
                DOWNLINK_QUEUE.put(["CH", "CM", "EN"])

                #enable
                enable(True)

            #raises the MCU a specified amount, disables automation
            elif cmd[:5] == "RAISE":
                #string parse to get amount to move
                cm = float(cmd.split(",")[1])/10

                #downlink
                logging.warning("Raising the MCU by %scm" % cm)
                DOWNLINK_QUEUE.put(["CH", "CM", "RS"+str(cm)])

                #disable automation
                EXIT_MOTOR_AUTOMATION = True

                #move
                enable(True)
                move(cm, "up", DOWNLINK_QUEUE)
                enable(False)

            #auto raise the MCU a specified amount, does NOT disable automation
            elif cmd[:10] == "AUTO_RAISE":
                #string parse to get amount to move
                cm = float(cmd.split(",")[1])/10

                #downlink
                logging.warning("Raising the MCU by %scm" % cm)
                DOWNLINK_QUEUE.put(["CH", "CM", "RS"+str(cm)])

                #move
                enable(True)
                move(cm, "up", DOWNLINK_QUEUE)
                enable(False)

            #lowers the MCU a specified amount, disables automation
            elif cmd[:5] == "LOWER":
                #string parse to get amount to move
                cm = float(cmd.split(",")[1])/10

                #downlink
                logging.warning("Lowering the MCU by %scm" % cm)
                DOWNLINK_QUEUE.put(["CH", "CM", "LOW"+str(cm)])

                #disable automation
                EXIT_MOTOR_AUTOMATION = True

                #move
                enable(True)
                move(cm, "down", DOWNLINK_QUEUE)
                enable(False)

            #disable MCU automation
            elif cmd == "DISABLE_MCU_AUTO":
                #downlink
                logging.warning("DISABLE_MCU_AUTO command recieved")
                DOWNLINK_QUEUE.put(["CH", "CM", "DAUT"])

                #disable automation
                EXIT_MOTOR_AUTOMATION = True

            #Override Automation for specified amount of minutes
            elif cmd[:12] == "DISABLE_AUTO":
                #string parse to get minutes to override
                minutes = int(cmd.split(",")[1])

                #downlink
                logging.warning(str(minutes) + " minute automation override received")
                DOWNLINK_QUEUE.put(["CH", "CM", "AOR"+str(minutes)])

                #override
                AUTOMATION_OVERRIDE = True
                OVERRIDE_TIME = minutes * 60

            #Reset the motor status file to 0
            elif cmd == "RESET_STATUS":
                motor_status_file = open(MOTOR_STATUS_FILE, "a+")
                motor_status_file.write("RESET\n0\n")
                motor_status_file.close()

            #End the thread
            elif cmd == "TERM":
                logging.warning("Terminate command recieved, shutting down thread")
                DOWNLINK_QUEUE.put(["CH","TM","SDT"])
                loop_break = True
                break

            #error
            else:
                logging.error("Other command received: " + cmd)
                DOWNLINK_QUEUE.put(["CH", "UC", cmd])

        if loop_break:
            break

        time.sleep(1)

    #log and exit thread
    MOTOR_QUEUE.put("COMMAND_HANDLER_DEAD")
    logging.warning("Exiting thread")
    DOWNLINK_QUEUE.put(["CH","TM","DEAD"])


#for the motor_automation thread
def one_eye_sleep(wait_seconds):
    '''
    sleeps for wait_seconds while also looking for EXIT_MOTOR_AUTOMATION
    if EXIT_MOTOR_AUTOMATION is set to True, the function will exit
    accepts wait_seconds, which is the amount of time to sleep
    also uses global variable EXIT_MOTOR_AUTOMATION
    '''

    begin = time.time()
    end = begin + wait_seconds
    current = begin

    while end > current:
        time.sleep(1)
        #exit thread?
        if EXIT_MOTOR_AUTOMATION:
            #EXIT_MOTOR_AUTOMATION = False #variable might need to be imported as global
            return #end the thread

        current = time.time()
 

#for motor_automation thread
def at_float(interval, PRESSURE_DATA_QUEUE):
    '''
    determines, using pressure data, whether the payload is at float
    first, empty the lifo-queue full of pressure data so that we are getting the most recent data
    then, average the pressure data over interval seconds
    if the average is less than the threshold, return True, otherwise False
    accepts the interval to average data over, and the PRESSURE_DATA_QUEUE to get the data from
    also uses AUTOMATION_THRESHOLD, a global variable
    '''

    start_time = time.time()

    #initialize variables
    tests = 0
    pressure_total = 0

    #empty the lifo-queue
    while not PRESSURE_DATA_QUEUE.empty():
        PRESSURE_DATA_QUEUE.get()

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        #EXIT_MOTOR_AUTOMATION = False
        return False #end the thread

    #add up data to average
    while time.time() < start_time + interval:
        pressure_total += PRESSURE_DATA_QUEUE.get()
        one_eye_sleep(11) #time should be slightly longer than PRESSURE_INTERVAL from sensors
        tests += 1

    #get average
    pressure_total /= tests

    #return
    if pressure_total < AUTOMATION_THRESHOLD:
        return True #yes
    else:
        return False #no


#for motor_automation thread
def auto_lower(DOWNLINK_QUEUE, MOTOR_QUEUE):
    '''
    this function downlinks that the motor will be lowering in OVERRIDE_TIME and
    then waits for the user to uplink an automation override.
    If the override is recieved, it waits again, if not, it lowers the MCU
    Accepts DOWNLINK_QUEUE for downlink and MOTOR_QUEUE to send the lower command
    Also uses global variables AUTOMATION_OVERRIDE, OVERRIDE_TIME, EXIT_MOTOR_AUTOMATION, and LOWER_AUTOMATION_TIME
    '''

    #global variables
    global AUTOMATION_OVERRIDE
    global OVERRIDE_TIME
    global EXIT_MOTOR_AUTOMATION

    OVERRIDE_TIME = LOWER_AUTOMATION_TIME

    #downlink
    logging.log(999,"Auto lowering MCU in " + str(OVERRIDE_TIME / 60) + " minutes pending override")
    DOWNLINK_QUEUE.put(["MA", "SR", "LMCU" + str(OVERRIDE_TIME / 60)]) #Auto-lowering in 1 hour

    #sleep
    one_eye_sleep(OVERRIDE_TIME)

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        #EXIT_MOTOR_AUTOMATION = False
        return #end the thread

    while AUTOMATION_OVERRIDE:
        logging.warning("Recieved override")
        AUTOMATION_OVERRIDE = False

        #downlink
        logging.log(999,"Auto lowering MCU in " + str(OVERRIDE_TIME / 60) + " minutes pending override")
        DOWNLINK_QUEUE.put(["MA", "SR", "LMCU" + str(OVERRIDE_TIME / 60)]) #Auto-lowering in 30 min

        #sleep
        one_eye_sleep(OVERRIDE_TIME)

        #exit thread?
        if EXIT_MOTOR_AUTOMATION:
            #EXIT_MOTOR_AUTOMATION = False
            return #end the thread

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        #EXIT_MOTOR_AUTOMATION = False
        return #end the thread

    #get distance to lower
    motor_status_file = open(MOTOR_STATUS_FILE, "a+")
    lines = motor_status_file.readlines()
    status = float(lines[len(lines)-1])
    status += 0.1
    status *= 10

    #downlink
    logging.warning("Auto-lowering the MCU, putting command in queue")
    DOWNLINK_QUEUE.put(["MA", "SR", "AL"]) #Auto-lowering the MCU
    MOTOR_QUEUE.put("LOWER," + str(status)) #Put command to lower motor in queue


#for motor_automation thread
def auto_raise(DOWNLINK_QUEUE, MOTOR_QUEUE):
    '''
    this function downlinks that the motor will be raising in OVERRIDE_TIME and
    then waits for the user to uplink an automation override.
    If the override is recieved, it waits again, if not, it lowers the MCU
    Accepts DOWNLINK_QUEUE for downlink and MOTOR_QUEUE to send the raise command
    Also uses global variables AUTOMATION_OVERRIDE, OVERRIDE_TIME, EXIT_MOTOR_AUTOMATION, and RAISE_AUTOMATION_TIME
    '''

    #global variables
    global AUTOMATION_OVERRIDE
    global OVERRIDE_TIME
    global EXIT_MOTOR_AUTOMATION

    OVERRIDE_TIME = RAISE_AUTOMATION_TIME

    #downlink
    logging.log(999,"System believes we are at float, auto-raising in " + str(OVERRIDE_TIME / 60) + " minutes pending override")
    DOWNLINK_QUEUE.put(["MA", "SR", "FL" + str(OVERRIDE_TIME / 60)])

    #sleep
    one_eye_sleep(OVERRIDE_TIME)

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        #EXIT_MOTOR_AUTOMATION = False
        return #end the thread

    while AUTOMATION_OVERRIDE:
        logging.warning("Recieved override")
        AUTOMATION_OVERRIDE = False

        #downlink
        logging.log(999,"Auto-raising in " + str(OVERRIDE_TIME / 60) + " minutes pending override")
        DOWNLINK_QUEUE.put(["MA", "SR", "FL" + str(OVERRIDE_TIME / 60)])

        #sleep
        one_eye_sleep(OVERRIDE_TIME)

        #exit thread?
        if EXIT_MOTOR_AUTOMATION:
            #EXIT_MOTOR_AUTOMATION = False
            return #end the thread

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        #EXIT_MOTOR_AUTOMATION = False
        return #end the thread

    #get distance to raise
    motor_status_file = open(MOTOR_STATUS_FILE, "a+")
    lines = motor_status_file.readlines()
    status = float(lines[len(lines)-1])
    status = 10 - status
    status *= 10

    #downlink
    logging.warning("Auto-raising the MCU, putting command in queue")
    DOWNLINK_QUEUE.put(["MA", "SR", "AR"])
    MOTOR_QUEUE.put("AUTO_RAISE,"+str(status)) #Put command to raise motor in queue


#worker function for motor_automation thread
def motor_automation(DOWNLINK_QUEUE, PRESSURE_DATA_QUEUE, MOTOR_QUEUE):
    '''
    This thread automates the payload through several steps:
        1. Sleep for ASCENT_TIME seconds
        2. Evaluate whether payload is at float by averaging pressure data
        3. If at float, alert the user via downlink and wait until there is no override
        4. Auto raise the MCU
        5. Sleep for FLOAT_TIME seconds
        6. Alert the user via downlink that it is time to close and wait until there is no override
        7. Auto close the MCU
        8. End the thread
    During all these check if the thread has recieved an end thread command and exit if it has
    Accepts DOWNLINK_QUEUE for downlink, PRESSURE_DATA_QUEUE for pressure data, and MOTOR_QUEUE to give commands
    Also uses global variables AUTOMATION_OVERRIDE and EXIT_MOTOR_AUTOMATION
    '''

    #downlink bootup
    logging.info("Thread initialized")
    DOWNLINK_QUEUE.put(["MA", "BU", "AUTO"])

    #global variables
    global AUTOMATION_OVERRIDE
    global EXIT_MOTOR_AUTOMATION

    floating = False

    #sleep until enough time has passed to think we are at float
    one_eye_sleep(ASCENT_TIME)

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
        EXIT_MOTOR_AUTOMATION = False
        logging.warning("Exiting the thread")
        DOWNLINK_QUEUE.put(["MA", "TM", "DEAD"])
        return #end the thread

    #downlink
    logging.warning("Ascent_time has passed, evaluating whether we are at float using pressure")
    DOWNLINK_QUEUE.put(["MA", "SR", "ATHP"])

    while not floating:
        #evaluate whether pressure data says we are at float for ten minutes
        floating = at_float(PRESSURE_EVALUATE_TIME, PRESSURE_DATA_QUEUE)

        #exit thread?
        if EXIT_MOTOR_AUTOMATION:
            EXIT_MOTOR_AUTOMATION = False
            logging.warning("Exiting the thread")
            DOWNLINK_QUEUE.put(["MA", "TM", "DEAD"])
            return #end the thread

    #auto raise the MCU
    auto_raise(DOWNLINK_QUEUE, MOTOR_QUEUE)

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
            EXIT_MOTOR_AUTOMATION = False
            logging.warning("Exiting the thread")
            DOWNLINK_QUEUE.put(["MA", "TM", "DEAD"])
            return #end the thread

    #sleep through float time
    one_eye_sleep(FLOAT_TIME)

    #exit thread?
    if EXIT_MOTOR_AUTOMATION:
            EXIT_MOTOR_AUTOMATION = False
            logging.warning("Exiting the thread")
            DOWNLINK_QUEUE.put(["MA", "TM", "DEAD"])
            return #end the thread

    #auto lower the MCU
    auto_lower(DOWNLINK_QUEUE, MOTOR_QUEUE)

    #downlink and log, then quit thread
    logging.warning("Exiting the thread")
    DOWNLINK_QUEUE.put(["MA", "TM", "DEAD"])


#worker function for the motor thread
def main(DOWNLINK_QUEUE, SYSTEM_QUEUE, PRESSURE_DATA_QUEUE, MOTOR_QUEUE):
    '''
    The main function for the motor thread
    Creates command_handler and motor_automation threads and then waits to kill them
    Accepts DOWNLINK_QUEUE for downlink, SYSTEM_QUEUE to alert main that the thread is dead,
    PRESSURE_DATA_QUEUE to evaluate whether the payload is at float, and MOTOR_QUEUE, which it
    searches for commands
    '''
    #downlink bootup
    logging.info("Thread initialized")
    DOWNLINK_QUEUE.put(["MO", "BU", "MOTR"])

    #build needed queues
    COMMAND_HANDLER_QUEUE = Queue.Queue()
    MOTOR_AUTOMATION_QUEUE = Queue.Queue()

    #package arguments
    COMMAND_HANDLER_ARGS = (DOWNLINK_QUEUE, COMMAND_HANDLER_QUEUE, MOTOR_QUEUE)
    MOTOR_AUTOMATION_ARGS = (DOWNLINK_QUEUE, PRESSURE_DATA_QUEUE, MOTOR_QUEUE)

    #holds all the threads
    threads = []

    #create the threads and add to the list
    threads.append(threading.Thread(name="command_handler", target=command_handler, args=COMMAND_HANDLER_ARGS))
    threads.append(threading.Thread(name='motor_automation',target=motor_automation, args=MOTOR_AUTOMATION_ARGS))

    #thread alive variables
    COMMAND_HANDLER_ALIVE = True
    MOTOR_AUTOMATION_ALIVE = False

    motor_init() #initialize the motor, NOTE: the motor is not enabled yet

    #start threads
    for t in threads:
        t.daemon = True
        logging.info("Started " + t.getName())
        DOWNLINK_QUEUE.put(["MO","BU",t.getName()])
        t.start()
    while True:
        while not MOTOR_QUEUE.empty():
            cmd = MOTOR_QUEUE.get()

            #For shutdown or reboot
            if cmd == "TERM":
                logging.warning("Terminate command recieved, alerting sub-threads to shut down")
                DOWNLINK_QUEUE.put(["MO","TM","AL"])

                #tell threads to terminate
                COMMAND_HANDLER_QUEUE.put("TERM")
                MOTOR_AUTOMATION_QUEUE.put("TERM")

            #check if sub-threads are dead
            elif cmd == "COMMAND_HANDLER_DEAD":
                COMMAND_HANDLER_ALIVE = False
            elif cmd == "MOTOR_AUTOMATION_DEAD":
                MOTOR_AUTOMATION_ALIVE = False
            else:
                logging.info("other command recieved: " + cmd + ". Sending command to command handler")
                COMMAND_HANDLER_QUEUE.put(cmd)
                DOWNLINK_QUEUE.put(["MO","UC",cmd])

        #if all threads are dead, exit the while loop and end the function
        if not COMMAND_HANDLER_ALIVE and not MOTOR_AUTOMATION_ALIVE: #and threading.activeCount() == 1:
            logging.warning("All sub-threads dead, shutting down thread")
            DOWNLINK_QUEUE.put(["MO","TM","STD"])
            break

        time.sleep(1)

    #log, downlink, and exit thread
    SYSTEM_QUEUE.put("MOTOR_DEAD")
    logging.warning("Exiting thread")
    DOWNLINK_QUEUE.put(["SE","TM","DEAD"])


#test script
def test_script():
    '''
    put a motor test script in this function and run motor.py as normal to run the script
    '''

    DOWNLINK_QUEUE = queue.Queue()
    motor_init()
    enable()
    while True:
        i = -1
        while i != 0 and i != 1:
            i = int(input("0 to move up, 1 to move down, 2 to disable motor, 3 to enable motor"))
            if i == 0:
                #i = int(i)
                direction = "up"
                print("up!")
            elif i == 1:
                #i = int(i)
                direction = "down"
                print("down!")
            elif i ==2:
                enable(False)
            elif i == 3:
                enable(True)
            else:
                print("Try again")

        dist = -1
        while dist < 0:
            dist = int(input("How many mm? "))
            if dist < 0:
                print("Try again")

        move(dist/10, direction, DOWNLINK_QUEUE)

    GPIO.cleanup()



if __name__ == '__main__':
	test_script()

