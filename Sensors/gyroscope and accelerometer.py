#!/usr/bin/python
import smbus
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for Revision 1
address = 0x68       # via i2cdetect
 
# Activate to be able to address the module
bus.write_byte_data(address, power_mgmt_1, 0)
def gyroscope():
    
    print("Gyroscope")
    print("---------------------")
 
    gyroscope_Xout = read_word_2c(0x43)
    gyroscope_Yout = read_word_2c(0x45)
    gyroscope_Zout = read_word_2c(0x47)
 
    print("gyroscope_Xout: ", ("%5d" % gyroscope_Xout), " Scaled: ", (gyroscope_Xout / 131))
    print("gyroscope_Yout: ", ("%5d" % gyroscope_Yout), " Scaled: ", (gyroscope_Yout / 131))
    print("gyroscope_Zout: ", ("%5d" % gyroscope_Zout), " Scaled: ", (gyroscope_Zout / 131))

def accelerometer():
    print()
    print("Accelerometer")
    print("---------------------")
     
    Acceleration_Xout = read_word_2c(0x3b)
    Acceleration_Yout = read_word_2c(0x3d)
    Acceleration_Zout = read_word_2c(0x3f)
     
    Acceleration_Xout_scaled = Acceleration_Xout / 16384.0
    Acceleration_Yout_scaled = Acceleration_Yout / 16384.0
    Acceleration_Zout_scaled = Acceleration_Zout / 16384.0
     
    print ("Acceleration_Xout: ", ("%6d" % Acceleration_Xout), " Scaled: ", Acceleration_Xout_scaled)
    print ("Acceleration_Yout: ", ("%6d" % Acceleration_Yout), " Scaled: ", Acceleration_Yout_scaled)
    print ("Acceleration_Zout: ", ("%6d" % Acceleration_Zout), " Scaled: ", Acceleration_Zout_scaled)
     
    print ("X Rotation: " , get_x_rotation(Acceleration_Xout_scaled, Acceleration_Yout_scaled, Acceleration_Zout_scaled))
    print ("Y Rotation: " , get_y_rotation(Acceleration_Xout_scaled, Acceleration_Yout_scaled, Acceleration_Zout_scaled))
    
if __name__ == '__main__':
    try:
        while True:
            gyros= gyroscope()
            accele=accelerometer()
            time.sleep(3)

    except KeyboardInterrupt:
        #turn off buzzer with interrupt
        GPIO.output(buzzer,GPIO.LOW)
        print("keyboard stop")
        GPIO.cleanup()    