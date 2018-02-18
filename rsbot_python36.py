from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import json


turningSpeedActuallyUsed = 255
#drivingSpeedAcutallyUsed = 255
turnDelay = 0.2
drivingSpeed = 255
straightDelay = 0.5




def runMotor(motorIndex, direction):
    motor = mh.getMotor(motorIndex+1)
    if direction == 1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -1:
        motor.setSpeed(drivingSpeed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    if direction == 0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.FORWARD)
    if direction == -0.5:
        motor.setSpeed(128)
        motor.run(Adafruit_MotorHAT.BACKWARD)



# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)




def times(lst, number):
                    return [x*number for x in lst]
    



def init(forwardDefinition, leftDefinition, pEnabled):

                global left
                global right
                global forward
                global backward
                global motorA
                global motorB
                global pingpongEnabled
                global mhPingPong
                pingpongEnabled = pEnabled
                forward = forwardDefinition
                backward = times(forward, -1)
                left = leftDefinition
                right = times(left, -1)
                print("directions", forward, backward, left, right)


                atexit.register(turnOffMotors)
                motorA = mh.getMotor(1)
                motorB = mh.getMotor(2)
                        
                
                atexit.register(turnOffMotors)

                if pingpongEnabled:
                    mhPingPong = Adafruit_MotorHAT(addr=0x61)
                

def turnOffMotors():

    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)    
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
                
   

def move(command):

                d = 255
    
                motorA.setSpeed(255)
                motorB.setSpeed(255)
                if command == 'F':
                    drivingSpeed = d
                    for motorIndex in range(4):
                        runMotor(motorIndex, forward[motorIndex])
                    time.sleep(straightDelay)
                if command == 'B':
                    drivingSpeed = d
                    for motorIndex in range(4):
                        runMotor(motorIndex, backward[motorIndex])
                    time.sleep(straightDelay)
                if command == 'L':
                    drivingSpeed = turningSpeedActuallyUsed
                    for motorIndex in range(4):
                        runMotor(motorIndex, left[motorIndex])
                    time.sleep(turnDelay)
                if command == 'R':
                    drivingSpeed = turningSpeedActuallyUsed
                    for motorIndex in range(4):
                        runMotor(motorIndex, right[motorIndex])
                    time.sleep(turnDelay)
                if command == 'U':
                    #mhArm.getMotor(1).setSpeed(127)
                    #mhArm.getMotor(1).run(Adafruit_MotorHAT.BACKWARD)
                    incrementArmServo(1, 10)
                    time.sleep(0.05)
                if command == 'D':
                    #mhArm.getMotor(1).setSpeed(127)
                    #mhArm.getMotor(1).run(Adafruit_MotorHAT.FORWARD)
                    incrementArmServo(1, -10)
                    time.sleep(0.05)
                if command == 'O':
                    #mhArm.getMotor(2).setSpeed(127)
                    #mhArm.getMotor(2).run(Adafruit_MotorHAT.BACKWARD)
                    incrementArmServo(2, -10)
                    time.sleep(0.05)
                if command == 'C':
                    #mhArm.getMotor(2).setSpeed(127)
                    #mhArm.getMotor(2).run(Adafruit_MotorHAT.FORWARD)
                    incrementArmServo(2, 10)
                    time.sleep(0.05)
                if command == 'FIRE':
                    pingPongMotor = mhPingPong.getMotor(1)
                    pingPongMotor.setSpeed(255)
                    pingPongMotor.run(Adafruit_MotorHAT.FORWARD)
                    time.sleep(2.8)
                    pingPongMotor.run(Adafruit_MotorHAT.RELEASE)

                
                turnOffMotors()




                

            

# routing

#{"F": forward, "B": back, "L": left, "R": right}
