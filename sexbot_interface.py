import os
import robot_util
import time
import atexit
import serial
import sys
import pigpio

straightSpeed=450
turnSpeed=500
straightDelay=0.5
stopDelay=0.05
turnDelay=0.4
ser=None
movementSystemActive=None
dildoActive=None
dildoDutyCycle1=10 #percentage
dildoDutyCycle2=20 #percentage
dildoDutyCycle3=30 #percentage
dildoFreq=25      #Hertz
dildoDelay=10     #seconds
pipwm=None        #object representing the pwm pin

def getSerial():
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
    return ser

def goForward(ser, speed):
    speedBytes=bytes(str(speed), encoding='ascii')+b'\r\n'
    ser.write(b'M1: '+speedBytes)
    ser.write(b'M2: '+speedBytes)

def goBackward(ser, speed):
    speedBytes=bytes(str(speed), encoding='ascii')+b'\r\n'
    ser.write(b'M1: -'+speedBytes)
    ser.write(b'M2: -'+speedBytes)

def turnRight(ser, speed):
    speedBytes=bytes(str(speed), encoding='ascii')+b'\r\n'
    ser.write(b'M1: -'+speedBytes)
    ser.write(b'M2: '+speedBytes)

def turnLeft(ser, speed):
    speedBytes=bytes(str(speed), encoding='ascii')+b'\r\n'
    ser.write(b'M1: '+speedBytes)
    ser.write(b'M2: -'+speedBytes)

def stopMotors(ser):
    ser.write(b'M1: 0\r\n')
    ser.write(b'M2: 0\r\n')

def exitTasks():
    global ser
    global pipwm
    pipwm.hardware_PWM(18,0,0)
    stopMotors(ser)
    ser.close()

def init():
    global ser
    global movementSystemActive
    global pipwm
    global dildoActive

    ser=getSerial()
    movementSystemActive=False
    dildoActive=False
    pipwm=pigpio.pi()
    atexit.register(exitTasks)
    pipwm.hardware_PWM(18,0,0)

def handleCommand(command, keyPosition):
    global straightSpeed
    global turnSpeed
    global turnDelay
    global straightDelay
    global ser
    global movementSystemActive
    global pipwm
    global dildoActive

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
            goForward(ser, straightSpeed)
            time.sleep(straightDelay)
            stopMotors(ser)
#            time.sleep(stopDelay)
            movementSystemActive=False

    if command == 'B':
        if movementSystemActive:
            print("skip")
        else:
            print("onback")
            movementSystemActive=True
            goBackward(ser, straightSpeed)
            time.sleep(straightDelay)
            stopMotors(ser)
#            time.sleep(stopDelay)
            movementSystemActive=False

    if command == 'L':
        if movementSystemActive:
            print("skip")
        else:
            print("onleft")
            movementSystemActive=True
            turnLeft(ser, turnSpeed)
            time.sleep(turnDelay)
            stopMotors(ser)
#            time.sleep(stopDelay)
            movementSystemActive=False

    if command == 'R':
        if movementSystemActive:
            print("skip")
        else:
            print("onright")
            movementSystemActive=True
            turnRight(ser, turnSpeed)
            time.sleep(turnDelay)
            stopMotors(ser)
#            time.sleep(stopDelay)
            movementSystemActive=False
    if command[0:6] == 'THRUST':
        if dildoActive:
            print('skip')
        else:
            dildoActive=True
            dildoDutyCycle=int(command[6:])
            pipwm.hardware_PWM(18, dildoFreq, dildoDutyCycle*10000)
            time.sleep(dildoDelay)
            pipwm.hardware_PWM(18, dildoFreq, 0)
            dildoActive=False



