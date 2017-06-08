import time
import datetime
from zlib import adler32
import sys
sys.path.append('/home/pi/miura')
from dwlk import dwlk

def main():
	while True:
		timestamp = "{0:.2f}".format(time.time())
		packet = "CU " + "MI " + str(timestamp) + ' '
		checksum = adler32(packet.encode('utf-8')) & 0xffffffff
		packet = packet + str(checksum)
		print(packet)
		packet = packet + '\n'
		dwlk.q.put(packet)
		time.sleep(1)
