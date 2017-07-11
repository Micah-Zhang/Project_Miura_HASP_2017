import time

## Turns on command LED after a command has been received, serv will turn it off
#def setcmdLED(cmdLED):
#    if not cmdLED.is_set():
#        cmdLED.set()
#    return

def main(downlink, ground, moto_cmd, run_exp):
	downlink.put(["UP", "BU", "UPLK"]) # Verifies correct thread initialization
	ground.flushInput() # Clears the serial communication channel before attempting to use it
	while True:
		time.sleep(2)
		if ground.inWaiting(): # Reads uplink command
			#HASP will send a series of 7 bytes
			# See Interface Manual for more Details
			soh = ground.read()  # Start of Heading (SOH)
			stx = ground.waitByte() # Start of Text (STX)
			tar = ground.waitByte() # Command  Byte: Target (specifies which thread should receive the command)
			cmd = ground.waitByte() # Command Byte: Contains actual uplink command
			etx = ground.waitByte() # End of Text (ETX)
			cr_ = ground.waitByte() # Carriage Return (CR)
			lf_ = ground.waitByte() # Line Feed (LF)
			packet = hex(int.from_bytes((soh + stx + tar + cmd + etx), byteorder='big')) # Convert from hex into bytes
			#print(packet)
			#setcmdLED(cmdLED) # Not sure if this is needed
			if soh == b"\x01" and etx == b"\x03":
				if stx == b"\x02":
					if tar == b"\xAA": # Ping Pi
						# Pings payload to test communication
						downlink.put(["UP","AK","ACK"])
					elif tar == b"\xBB": # Send command to moto thread to be processed
						moto_cmd.put(cmd)
					#elif tar == b"\xCD": # Manual Extension and Retraction
					#	# Tells stepper motor to travel to specified location
					#elif tar == b"\xCC":
					#	if cmd == b"\x03": # Query Safe Mode
					#	elif cmd == b"\x04": # Safe Mode ON
					#		# Halts Motor
					#	elif cmd == b"\x05": # Safe Mode OFF
					#		 # Restarts Extension Cycle
					#elif tar == b"\xDD": # Reboot Pi
					#elif tar == b"\xEE": # Send Low Resolution Image
					else:
						downlink.put(["UP", "ER", packet]) # Command not recognized. Downlink error message.
				elif stx == b"\x30": # Not sure why this is.
					pass
				else:
					downlink.put(["UP", "ER", packet]) # Start of text byte not  recognized. Downlink error message.
			else:
				downlink.put(["UP", "ER", packet]) # Received unrecognized bytes. Downlink error message.
		return 0
