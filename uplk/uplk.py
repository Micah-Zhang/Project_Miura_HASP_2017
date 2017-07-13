import time

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
			if soh == b"\x01" and etx == b"\x03":
				if stx == b"\x02":

					if tar == b"\xAA": #Ping Pi
						downlink.put(["UP","AK","ACK"])
					elif tar == b"\xBB": #Send command to moto thread to be processed
						if cmd == b"\x01": #Calibrate motor count at bottom
							moto_cmd.put(cmd)
						elif cmd == b"\x02": #Calibrate motor count at top
							moto_cmd.put(cmd)
					elif tar == b"\xCB":
						nudge = int.from_bytes(cmd, byteorder='big')
						if nudge > 100:
							downlink.put(["UP","ER",packet]) #downlink error packet
						else:
							moto_cmd.put(nudge)
					elif tar == b"\xCA": #Nudge up percentage
						nudge = int.from_bytes(cmd,byteorder='big')
						if nudge > 100:
							downlink.put(["UP","ER",packet])
						else:
							nudge = nudge += 101 #necessary to retain nudge 0
							moto_cmd.put(nudge)
					elif tar == b"\xCD": #Nudge down percentage
						nudge = - int.from_bytes(cmd,byteorder='big')
						if abs(nudge) > 100:
							downlink.put(["UP"."ER",packet])
						else:
							nudge = nudge -= 101
							moto_cmd.put(nudge)
					else:
						downlink.put(["UP", "ER", packet]) #Command not recognized. Downlink error message.

				elif stx == b"\x30":
					pass
				else:
					downlink.put(["UP", "ER", packet]) # Start of text byte not  recognized. Downlink error message.
			else:
				downlink.put(["UP", "ER", packet]) # Received unrecognized bytes. Downlink error message.
		return 0
