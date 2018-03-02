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

import time
import subprocess
import RPi.GPIO as GPIO

led_pin = 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.output(led_pin,False)

def main(downlink, ground, moto_cmd, safe_mode):
	downlink.put(["UP", "BU", "UPLK"]) # Verifies correct thread initialization
	led_on = False
	ground.flushInput() # Clears the serial communication channel before attempting to use it
	while True:
		if led_on:
			GPIO.output(led_pin,True)
			led_on = False
		elif not led_on:
			GPIO.output(led_pin,False)
		if ground.inWaiting(): # Reads uplink command
			led_on = True
			#HASP will send a series of 7 bytes
			# See Interface Manual for more Details
			soh = ground.read()  # Start of Heading (SOH)
			stx = ground.waitByte() # Start of Text (STX)
			tar = ground.waitByte() # Command  Byte: Target (specifies which thread should receive the command)
			cmd = ground.waitByte() # Command Byte: Contains actual uplink command
			etx = ground.waitByte() # End of Text (ETX)
			cr_ = ground.waitByte() # Carriage Return (CR)
			lf_ = ground.waitByte() # Line Feed (LF)
			print("2 byte command received: ", tar, cmd)
			packet = hex(int.from_bytes((soh + stx + tar + cmd + etx), byteorder='big')) # Convert from hex into bytes
			print(packet)
			if soh == b"\x01" and etx == b"\x03":
				if stx == b"\x02":
					if tar == b"\xAA": #Ping Pi
						downlink.put(["UP","AK","ACK"])
					elif tar == b"\xBA": #Send command to moto thread to be processed
						moto_cmd.put(cmd)
						print("passing cmd to motor thread")
					elif tar == b"\xCA": #Nudge absolute percentage
						nudge = int.from_bytes(cmd, byteorder='big')
						if nudge > 100:
							downlink.put(["UP","ER",packet]) #downlink error packet
						else:
							moto_cmd.put(nudge)
							print("nudge command typeA sent! Nudging: ", nudge)
					elif tar == b"\xDA": #Nudge up relative percentage
						nudge = int.from_bytes(cmd,byteorder='big')
						if nudge > 100:
							downlink.put(["UP","ER",packet])
						else:
							nudge += 101 #necessary to retain nudge 0
							moto_cmd.put(nudge)
							print("nudge command typeB sent")
					elif tar == b"\xEA": #Nudge down relative percentage
						nudge = - int.from_bytes(cmd,byteorder='big')
						if abs(nudge) > 100:
							downlink.put(["UP","ER",packet])
						else:
							nudge -= 101
							moto_cmd.put(nudge)
							print("nudge command typeB sent")
					elif tar == b"\xFA": #change cycle count
						count = int.from_bytes(cmd,byteorder='big')
						if count > 54:
							downlink.put(["UP","ER",packet])
						else:
							count += 202
							moto_cmd.put(count)
					elif tar == b"\xBB":
						if cmd == b"\x00": # safe mode OFF
							safe_mode.clear()
							moto_cmd.put(b'\x08')
						elif cmd == b"\x01": # safe mode ON
							safe_mode.set()
							moto_cmd.put(b'\x07')
					elif tar == b"\xDB": # reboot pi
						subprocess.Popen('sudo reboot', shell=True)
					else:
						downlink.put(["UP", "ER", packet]) #Command not recognized. Downlink error message.
				elif stx == b"\x30":
					pass
				else:
					downlink.put(["UP", "ER", packet]) # Start of text byte not  recognized. Downlink error message.
			else:
				downlink.put(["UP", "ER", packet]) # Received unrecognized bytes. Downlink error message.
		time.sleep(1)
