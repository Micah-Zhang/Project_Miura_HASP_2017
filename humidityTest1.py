import time
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import urllib2

sensor = Adafruit_DHT.DHT22
pin = 2
myAPI = "XXXXXXXXXXXXXXX"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' %myAPI

GPIO.setmode(GPIO.BCM)

while 1:
    print ("------------------------------")
    humidity, temperature = Adafruit_DHT.read_rety(sensor, pin)
    desturl = baseURL + "&field1={0}&field2={1}".format(temperature,humidity)
    f=urllib2.urlopen(desturl)
    f.close()
    print (temperature)
    print (humidity)
    time.sleep(1)
    
