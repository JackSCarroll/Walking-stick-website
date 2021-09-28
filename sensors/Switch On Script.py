import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
import subprocess
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Script1 = '/home/pi/Desktop/Final/DistanceBuzzer.py'
Script2 = '/home/pi/Desktop/Final/GyroscopeAccelerometer.py'

try:
    while True:
        if GPIO.input(16) == False:
            print("on")
            print("Running the distance and gyro")
            subprocess.run("python3 " + Script1 + " & python3 " + Script2, shell=True)
except KeyboardInterrupt:
    print("interrupt")