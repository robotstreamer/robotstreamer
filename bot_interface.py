import os
import robot_util
import time
import atexit
import serial
import sys
import pigpio

commandArgs = None

#straight speeds 200#300#450
#turn speeds 500#700#450

straightDelay=0.6
stopDelay=0.05
turnDelay=0.5
ser=None
movementSystemActive=None
actuatorActive=None
actuatorDutyCycle1=10 #percentage
actuatorDutyCycle2=20 #percentage
actuatorDutyCycle3=30 #percentage
actuatorFreq=25      #Hertz
actuatorDelay=3      #seconds
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

def init(cArgs):
    global ser
    global movementSystemActive
    global pipwm
    global actuatorActive
    global commandArgs

    ser=getSerial()
    movementSystemActive=False
    actuatorActive=False
    pipwm=pigpio.pi()
    atexit.register(exitTasks)
    pipwm.hardware_PWM(18,0,0)

    commandArgs = cArgs

    
def handleCommand(command, keyPosition, price=0):
    global turnDelay
    global straightDelay
    global ser
    global movementSystemActive
    global pipwm
    global actuatorActive

    print("\n\n")

    if keyPosition != "down":
        return

    robot_util.handleSoundCommand(command, keyPosition, price)

    if command == 'F':
        if movementSystemActive:
            print("skip")
        else:
            print("onforward")
            movementSystemActive=True
            goForward(ser, commandArgs.straight_speed)
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
            goBackward(ser, commandArgs.straight_speed)
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
            turnLeft(ser, commandArgs.turn_speed)
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
            turnRight(ser, commandArgs.turn_speed)
            time.sleep(turnDelay)
            stopMotors(ser)
#            time.sleep(stopDelay)
            movementSystemActive=False
    if command[0:6] == 'THRUST':
        if actuatorActive:
            print('skip')
        else:
            actuatorActive=True
            actuatorDutyCycle=int(command[6:])
            pipwm.hardware_PWM(18, actuatorFreq, actuatorDutyCycle*10000)
            time.sleep(actuatorDelay)
            pipwm.hardware_PWM(18, actuatorFreq, 0)
            actuatorActive=False



