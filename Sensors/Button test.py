import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
import paho.mqtt.client as mqtt 
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
address = 'you are on x street'


hostname = "mqtt://broker.hivemq.com"
client = mqtt.Client(hostname, True, None, mqtt.MQTTv31)
client.connect(hostname, port=1883, keepalive=60, bind_address="")
client.subscribe("/gps/device/0")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message=on_message
client.loop_forever()


while True: # Run forever
    #print("running")
    if GPIO.input(21) == False:
        print("Button was pushed!")
        os.system("/home/pi/./speech.sh " + address)
        time.sleep(1)