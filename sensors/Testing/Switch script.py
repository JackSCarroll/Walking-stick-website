import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os
import subprocess
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

Script1 = '/home/pi/Desktop/Final/DistanceBuzzer.py'
Script2 = '/home/pi/Desktop/Final/GyroscopeAccelerometer.py'

global Running
Running = True

try:
    while True:
        if GPIO.input(16) == True:
            print("off")
            if(Running):
                print("Killed two processes")
                os.system("pkill -9 -f DistanceBuzzer.py")
                os.system("pkill -9 -f GyroscopeAccelerometer.py")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped")
