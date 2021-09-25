#!/usr/bin/python
import smbus
import math
import time
import requests
import os
import smtplib

SMTP_SERVER ='smtp.gmail.com' #email server
SMTP_PORT = 587 #server port
GMAIL_USERNAME = 'smartwalkingstick01@gmail.com'
GMAIL_PASSWORD = 'WalkingStick01'

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

global falling
falling = False
fallingTime = 0

#X rotation under 30 means walking stick is flat on the ground
#over 30 means its somewhat up right
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    #Read Accelerometer and Gyro value in 16-bit
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    
    #link higher and lower value together in a chain/series
    value = ((h << 8) | l)
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    
#to get signed value from mpu6050
    if(val > 32768):
        return (val - 65536)
    else:
        return val

#function to calculate distance 
def dist(a,b):
    return math.sqrt((a*a)+(b*b)) # Return the square root of different numbers

#function to get rotation of y  
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z)) # Return the arc tangent of x and distance of y and z in radians
    return math.degrees(radians) # Convert from radians to degrees

#function to get rotation of x
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z)) # Return the arc tangent of y and distance of x and z in radians
    return math.degrees(radians) # Convert from radians to degrees
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for Revision 1 board
address = 0x68       # device address via i2cdetect
 
# Activate to be able to address the module
bus.write_byte_data(address, power_mgmt_1, 0)

class Emailer:
    def sendmail(self, recipient, subject, content):
          
        #Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
                   "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
  
        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
  
        #Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
  
        #Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
        session.quit
  
sender = Emailer()

   


def gyroscope():
    
    print("Gyroscope")
    print("---------------------")
 
    gyroscope_Xout = read_word_2c(0x43) #getting the raw value for x for gyroscope
    gyroscope_Yout = read_word_2c(0x45) #getting the raw value for y for gyroscope
    gyroscope_Zout = read_word_2c(0x47) #getting the raw value for z for gyroscope
    
    gyroscope_Xout_scaled = gyroscope_Xout / 32.8 #Full scale range +/- 1000 degree/C as per sensitivity scale factor of 131 LSB (Count)//s.
    gyroscope_Yout_scaled = gyroscope_Yout / 32.8 #Full scale range +/- 1000 degree/C as per sensitivity scale factor of 131 LSB (Count)//s.
    gyroscope_Zout_scaled = gyroscope_Zout / 32.8 #Full scale range +/- 1000 degree/C as per sensitivity scale factor of 131 LSB (Count)//s.
 
    print("gyroscope_Xout: ", ("%5d" % gyroscope_Xout), " Scaled: ", gyroscope_Xout_scaled) 
    print("gyroscope_Yout: ", ("%5d" % gyroscope_Yout), " Scaled: ", gyroscope_Yout_scaled)
    print("gyroscope_Zout: ", ("%5d" % gyroscope_Zout), " Scaled: ", gyroscope_Zout_scaled) 

def accelerometer():
    global falling
    # \n is placed to indicate EOL (End of Line)

    print()
    print("Accelerometer")
    print("---------------------")
     
    Acceleration_Xout = read_word_2c(0x3b) #getting the raw value for x for accelerometer
    Acceleration_Yout = read_word_2c(0x3d) #getting the raw value for y for accelerometer
    Acceleration_Zout = read_word_2c(0x3f) #getting the raw value for z for accelerometer
     
    #y = 1 = |
    #y = 0 = _
     
    Acceleration_Xout_scaled = Acceleration_Xout / 2048 #Full scale range of +/- 16g with Sensitivity Scale Factor of 16,384 LSB(Count)/g.
    Acceleration_Yout_scaled = Acceleration_Yout / 2048 #Full scale range of +/- 16g with Sensitivity Scale Factor of 16,384 LSB(Count)/g.
    Acceleration_Zout_scaled = Acceleration_Zout / 2048 #Full scale range of +/- 16g with Sensitivity Scale Factor of 16,384 LSB(Count)/g.
    
    Acceleration = math.sqrt(Acceleration_Xout_scaled**2 + Acceleration_Yout_scaled**2 + Acceleration_Zout_scaled**2)

    
    print ("Acceleration_Xout: ", ("%6d" % Acceleration_Xout), " Scaled: ", Acceleration_Xout_scaled)
    print ("Acceleration_Yout: ", ("%6d" % Acceleration_Yout), " Scaled: ", Acceleration_Yout_scaled)
    print ("Acceleration_Zout: ", ("%6d" % Acceleration_Zout), " Scaled: ", Acceleration_Zout_scaled)

    print("Acceleration: ", Acceleration)
#     Y.append(Acceleration_Yout)
     
    print ("X Rotation: " , get_x_rotation(Acceleration_Xout_scaled, Acceleration_Yout_scaled, Acceleration_Zout_scaled))
    print ("Y Rotation: " , get_y_rotation(Acceleration_Xout_scaled, Acceleration_Yout_scaled, Acceleration_Zout_scaled))
    
    # fall detection trigger using acceleration speed and aceleration position of x, y and z
    if (Acceleration > 11):
        #potentially falling
        falling = True
    
    #if the gyroscope is lying flat the alert is sent, to make sure warning is not sent just because sudden increase in acceleration as this will happen often,
    #because the person in on a walk
    #we chose to put condition lying flat because the position of the gyroscope in the walking cane will be standing position (|), so when it falls it will be in flat position (-)
    
    #if after potentially falling, and we get to a flat position, then we have fell.
    if(Acceleration_Xout_scaled < 1 and Acceleration_Yout_scaled < 3 and Acceleration_Zout_scaled > 1 and falling is True): 
        print("Someone_fell")
        sendTo = 'anthony8121999@gmail.com'
        emailSubject = "Someone fell"
        emailContent = "Hey there someone fell, please go to our website to find their location."
        sender.sendmail(sendTo, emailSubject, emailContent)
        print("Email Sent")
                    

if __name__ == '__main__':   
    try:
        while True:
            
            #gyros= gyroscope()
            accele=accelerometer()
            time.sleep(1)
            
            #if potentially falling, add time, at 5 seconds false alarm. in those 5 seconds it checks if the stick goes flat, which is called the fall detection function
            #in accelerometer
            if(falling):
                print("Someones falling maybe - " + str(fallingTime))
                fallingTime += 1
                
            if(fallingTime > 5):
                #its been 5 seconds and its not flat yet. probably haven't fallen
                falling = False
                fallingTime = 0
                

    except KeyboardInterrupt:
#         print("keyboard stop, debug:")
#         AddOne = 0
#         for i in Y:
#             TimeX.append(AddOne)
#             AddOne += 1
#             print(AddOne, ':', i, '\n')
#         plt.plot(TimeX, Y)
            
        GPIO.cleanup()    
