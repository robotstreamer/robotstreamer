import atexit
import robot_util
import PiMotor
import RPi.GPIO as GPIO
import os
import time

#how long a forward or reverse movement lasts in seconds
straightDelay=0.5
#how long a turn movement lasts in seconds
turnDelay=0.25
#tracks the state of the movement system globally
movementSystemActive=False

#gets called to turn on the motors and lights to turn right
def turnRight():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    ar.on()
    mfl.forward(100)
    mfr.reverse(100)
    mbl.forward(100)
    mbr.reverse(100)

    return

#gets called to turn on the motors and lights to turn left
def turnLeft():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    al.on()
    mfl.reverse(100)
    mfr.forward(100)
    mbl.reverse(100)
    mbr.forward(100)

    return

#gets called to turn on the motors and lights to go forward
def goForward():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    af.on()
    mfl.forward(100)
    mfr.forward(100)
    mbl.forward(100)
    mbr.forward(100)

    return

#gets called to turn on the motors and lights to go backward
def goBackward():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    ab.on()

    mfl.reverse(100)
    mfr.reverse(100)
    mbl.reverse(100)
    mbr.reverse(100)

    return

#gets called to turn off all motors and lights
def releaseMotors():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    af.off()
    al.off()
    ab.off()
    ar.off()
    mfl.stop()
    mfr.stop()
    mbl.stop()
    mbr.stop()

    return

#special function called only when the program stops using python's atexit feature
def motorshieldShutdown():
    releaseMotors()
    return

#gets called once by controller.py to initialize the interface
def init():
    global af
    global al
    global ab
    global ar
    global mfl
    global mfr
    global mbl
    global mbr

    ab = PiMotor.Arrow(1)
    al = PiMotor.Arrow(2)
    af = PiMotor.Arrow(3)
    ar = PiMotor.Arrow(4)
    #front left motor
    mfl=PiMotor.Motor("MOTOR2", 1)
    #front right motor
    mfr=PiMotor.Motor("MOTOR3", 1)
    #back left motor
    mbl=PiMotor.Motor("MOTOR1", 1)
    #back right motor
    mbr=PiMotor.Motor("MOTOR4", 1)
    atexit.register(motorshieldShutdown)

    return


#called by controller.py every time a command is sent
def handleCommand(command, keyPosition):
    global movementSystemActive

    print("\n\n\n\nhandleCommand called.\n")

    if keyPosition != "down":
      return
    robot_util.handleSoundCommand(command, keyPosition)
    if command == 'F':
        if movementSystemActive:
            print("skip")
        else:
            movementSystemActive=True
            goForward()
            time.sleep(straightDelay)
            releaseMotors()
            movementSystemActive=False

    if command == 'B':
        if movementSystemActive:
            print("skip")
        else:
            movementSystemActive=True
            goBackward()
            time.sleep(straightDelay)
            releaseMotors()
            movementSystemActive=False

    if command == 'L':
        if movementSystemActive:
            print("skip")
        else:
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

    return

