import os
import robot_util
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM
import time
import atexit

mh = Adafruit_MotorHAT(addr=0x6F)
pwm = PWM(0x6F)

#These are the on times that get sent to the pwm module to tell the servo how
#far to rotate. Duty cycle is onTime/4095. Set these to limit the range of
#motion to something sensible. Be sure the pan tilt doesn't bottom out or you
#can damage the servo.
panMinOnTime=125
panMaxOnTime=625
tiltMinOnTime=125
tiltMaxOnTime=575

#global variables to keep track of current percentage of tilt and pan
panPercentage=50.0
tiltPercentage=50.0

#Sets how big of a step each button press gives in percentage.
tiltIncrement=5
panIncrement=10.0/3.0

#Sets the duty cycle for the motors while moving. speed/255 is the duty cycle.
straightSpeed=255
turnSpeed=255

#Sets how long the motors turn on in seconds for movements.
straightDelay=0.4
turnDelay=0.1
movementSystemActive=False

def setTilt(percentage):
    onTime=int((tiltMaxOnTime-tiltMinOnTime)*(percentage/100.0)+tiltMinOnTime)
    if onTime > tiltMaxOnTime:
        onTime=tiltMaxOnTime
    elif onTime < tiltMinOnTime:
        onTime=tiltMinOnTime
    print("setTilt(",percentage,")")
    print("ontime=", onTime)
    pwm.setPWM(14, 0, onTime)

def setPan(percentage):
    onTime=int((panMaxOnTime-panMinOnTime)*(percentage/100.0)+panMinOnTime)
    if onTime > panMaxOnTime:
        onTime=panMaxOnTime
    elif onTime < panMinOnTime:
        onTime=panMinOnTime
    print("setPan(",percentage,")")
    print("ontime=", onTime)
    pwm.setPWM(15, 0, onTime)

def turnRight():
    leftMotor.setSpeed(turnSpeed)
    rightMotor.setSpeed(turnSpeed)
    leftMotor.run(Adafruit_MotorHAT.BACKWARD)
    rightMotor.run(Adafruit_MotorHAT.BACKWARD)

def turnLeft():
    leftMotor.setSpeed(turnSpeed)
    rightMotor.setSpeed(turnSpeed)
    leftMotor.run(Adafruit_MotorHAT.FORWARD)
    rightMotor.run(Adafruit_MotorHAT.FORWARD)

def goForward():
    leftMotor.setSpeed(straightSpeed)
    rightMotor.setSpeed(straightSpeed)
    leftMotor.run(Adafruit_MotorHAT.BACKWARD)
    rightMotor.run(Adafruit_MotorHAT.FORWARD)

def goBackward():
    leftMotor.setSpeed(straightSpeed)
    rightMotor.setSpeed(straightSpeed)
    leftMotor.run(Adafruit_MotorHAT.FORWARD)
    rightMotor.run(Adafruit_MotorHAT.BACKWARD)

#Turns off motors and the PWM
def motorhatShutdown():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    pwm.setPWM(14, 0, 0)
    pwm.setPWM(15, 0, 0)

#Turns off only the motors
def releaseMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def init():
    global leftMotor
    global rightMotor
    global panPercentage
    global tiltPercentage

    atexit.register(motorhatShutdown)
    leftMotor = mh.getMotor(1)
    rightMotor = mh.getMotor(2)
    pwm.setPWMFreq(60)
    setPan(50.0)
    setTilt(50.0)
    panPercentage=50.0
    tiltPercentage=50.0


def handleCommand(command, keyPosition):
    global movementSystemActive
    global tiltPercentage
    global panPercentage

    print("\n\n")

    if keyPosition != "down":
        return

    robot_util.handleSoundCommand(command, keyPosition)

    if command == 'F':
        if movementSystemActive:
            print("skip")
        else:
            print("onforward")
            movementSystemActive=True
            goForward()
            time.sleep(straightDelay)
            releaseMotors()
            movementSystemActive=False

    if command == 'B':
        if movementSystemActive:
            print("skip")
        else:
            print("onback")
            movementSystemActive=True
            goBackward()
            time.sleep(straightDelay)
            releaseMotors()
            movementSystemActive=False

    if command == 'L':
        if movementSystemActive:
            print("skip")
        else:
            print("onleft")
            movementSystemActive=True
            turnLeft()
            time.sleep(turnDelay)
            releaseMotors()
            movementSystemActive=False

    if command == 'R':
        if movementSystemActive:
            print("skip")
        else:
            print("onright")
            movementSystemActive=True
            turnRight()
            time.sleep(turnDelay)
            releaseMotors()
            movementSystemActive=False

    #The m in front of these events differentiates them from the v4l2 commands
    #because it is a mechanical pan and tilt. It is possible to have a robot
    #that responds to v4l2 pan and tilt and mechanical pan and tilt events.
    if command == 'mpan-':
        print("onmpan-")
        panPercentage+=panIncrement
        if panPercentage > 100.0:
            panPercentage=100.0
        setPan(panPercentage)

    if command == 'mpan+':
        print("onmpan+")
        panPercentage-=panIncrement
        if panPercentage < 0.0:
            panPercentage=0.0
        setPan(panPercentage)

    if command == 'mtilt-':
        print("onmtilt-")
        tiltPercentage+=tiltIncrement
        if tiltPercentage > 100.0:
            tiltPercentage=100.0
        setTilt(tiltPercentage)

    if command == 'mtilt+':
        print("onmtilt+")
        tiltPercentage-=tiltIncrement
        if tiltPercentage < 0.0:
            tiltPercentage=0.0
        setTilt(tiltPercentage)

