import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
import paho.mqtt.client as mqtt 
import threading
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
address = 'you are on x street'
#"/gps/device/0"
#"mqtt://broker.hivemq.com"
global outputstring
outputstring = ''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/gps/device/0")

def on_message(client, userdata, msg):
    global outputstring
    print(msg.topic+" "+str(msg.payload))
    outputstring = msg.payload

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

#client.loop_forever()

while True: # Run forever
    print("running")
    if GPIO.input(21) == False:
        lat = ''
        long = ''
        print("Button was pushed!")
        client.loop_start()
        time.sleep(1)
        client.loop_stop()
        outputstringTest = str(outputstring).split(',')
            
        lat = outputstringTest[0].split(':')[1]
        long = outputstringTest[1].split(':')[1][:-2]
       
        locator = Nominatim(user_agent="myGeocoder")
        coordinates = lat + ", " + long
        
        location = locator.reverse(coordinates)
        location.raw
        print(location.address)
        address = location.address
        
        

        os.system("/home/pi/./speech.sh " + "Your current location is " + address)
        time.sleep(1)