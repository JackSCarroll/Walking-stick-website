# Example code for PiicoDev Motion Sensor MPU6050
from PiicoDev_MPU6050 import PiicoDev_MPU6050

from time import sleep

motion = PiicoDev_MPU6050()

def gyros():
    # Gyroscope Data
    gyro = motion.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
    print()
    print("Gyroscope")
    print("---------------------")
    print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))
    
    
def accele():
    # Accelerometer data
    accel = motion.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    print()
    print("Accelerometer")
    print("---------------------")
    print("x:" + str(aX) + " y:" + str(aY) + " z:" + str(aZ))
    
if __name__ == '__main__':
    try:
        while True:
            gyroscope= gyros()
            accelerometer=accele()
            sleep(3)

    except KeyboardInterrupt:
        print("keyboard stop")
        GPIO.cleanup()   