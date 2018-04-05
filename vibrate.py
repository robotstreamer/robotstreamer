from math import sin
from robot_util import times
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time


vibrateSystemActive = False


def setMotorSpeed(mh, motorIndex, direction, s):
    motor = mh.getMotor(motorIndex+1)
    #print("direction", direction)
    if direction == 1:
        motor.setSpeed(s)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -1:
        motor.setSpeed(s)
        motor.run(Adafruit_MotorHAT.BACKWARD)





def vibrate(mh, forwardDefinition):

    global vibrateSystemActive
    
    if vibrateSystemActive:
        print("skip")
    else:

        vibrateSystemActive = True

        for i in range(20):
            a = float(i) / 1.0

            speed = int(sin(a) * 255.0) 
            print("speed", speed)
            
            if speed >= 0:
                directions = forwardDefinition
            else:
                directions = times(forwardDefinition, -1)
                speed = -speed

                
            print(speed, directions)
            for motorIndex in range(4):
                setMotorSpeed(mh,
                              motorIndex,
                              directions[motorIndex],
                              speed)
            time.sleep(0.05)
            
        
        turnOffMotors(mh)
        vibrateSystemActive = False



#todo: this function should be in a file shared by this and rsbot
def turnOffMotors(mh):

    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)    
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

        
        
def main():

    mh = Adafruit_MotorHAT(addr=0x60)
    vibrate(mh, [-1,1,-1,1])


if __name__ == "__main__":
    main()
    
