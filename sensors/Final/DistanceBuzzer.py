#Libraries
import RPi.GPIO as GPIO
import time
#for audio
import pygame
 
 
#sound file
pygame.mixer.init()
pygame.mixer.music.load("Beep.wav")


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

TooClose = 100 #cm away from the stick for beep
PollingTime = 0.5 #seconds between readings
 
#set GPIO Pins, dont change
GPIO_TRIGGER = 4
GPIO_ECHO = 17
buzzer=27

 
#set GPIO direction (IN / OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            
            if(dist < TooClose):
                print("Too CLOSE, make beeping sound")
                #buzzer
                #GPIO.output(buzzer,GPIO.HIGH)
                #sound file
                pygame.mixer.music.play()
            else:
                GPIO.output(buzzer,GPIO.LOW)
            time.sleep(PollingTime)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        #turn off buzzer with interrupt
        GPIO.output(buzzer,GPIO.LOW)
        print("keyboard stop")
        GPIO.cleanup()