import serial
import time
import _thread
import sys
import robot_util


try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
except Exception as e:
    print("serial error 1", e)

PASSIVE = b'\x80'
SAFE = b'\x83'
CLEAN = b'\x87'


def handleCommand(command, keyPosition, price=0):

    global lastCommand

    print("handling command")

    if command == 'L':
        ser.write("l\r".encode())
    elif command == 'R':
        ser.write("r\r".encode())
    elif command == 'F':
        ser.write("f\r".encode())
    elif command == 'B':
        ser.write("b\r".encode())
    ser.flush()


def init():
    try:
        print("init parallaxy")
        ser.write(PASSIVE)
        ser.write(SAFE)
    except Exception as e:
        print("serial error 2", e)
