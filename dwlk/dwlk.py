import time
from zlib import adler32

# Stores data from each thread in separate logs
def logdata(packet, sender):
	if sender == "MO": # Keeps track of all packets sent by the motor thread
		with open("/home/pi/moto.log", 'a') as log:
			log.write(packet)
		print(packet, end="")

	if sender == "UP": # Keeps track of all packets sent by the uplink thread
		with open("/home/pi/uplk.log", 'a') as log:
			log.write(packet)
		print(packet, end="")

	if sender == "SE": # Keeps track of all packets sent by the sensor thread
		with open("/home/pi/sens.log", 'a') as log:
			log.write(packet)
		print(packet, end="")

	if sender == "DW": # Keeps track of all packets sent by the downlink thread
		with open("/home/pi/dwlk.log", 'a') as log:
			log.write(packet)
		print(packet, end="")

def main(downlink, gnd):
	downlink.put(["DW", "BU", "DWNL"]) # Verify that thread has started successfully
	while True:
		# All downlinked data must be in this form:
		# [2 char sender, 2 char record type, string of data]
		# Multi-item data needs to be in the form of ###, ###, ###
		packet = downlink.get() # Pop the first item of the queue: a list of that contains the labels for the packet
		sender, record, data = packet[0], packet[1], str(packet[2]) # Package the elements of the popped list into three separate variables
		l = len(data) # Calculate the length of the data
#		print("pre-packet: ", packet)
		if type(data) is not bytes: # Necessary for sending strings
			a_data = data.encode('utf-8')
		else:
			a_data = data # Useful for sending raw data
		ck = adler32(a_data) & 0xffffffff # Use data to calculate checksum
		t = time.time()  # Unix time. Seconds since epoch.
		packet = "\x01CU MI %s %s %.2f %i %i\x02" % (sender, record, t, l, ck) + " " + data + "\x03\n" # Follows HASP guidelines
		with open("/home/pi/downlink.log", 'a') as log: # Keeps a central record of everything that was downlinked
			log.write(packet)
		gnd.write(packet) # Downlink packet through serial
#		print("post-packet: ", packet)	
		logdata(packet, sender) # Log data received
