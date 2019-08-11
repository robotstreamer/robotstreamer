import serial
import time
import _thread
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import robot_util


try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
except Exception as e:
    print("serial error 1", e)



RESET = b'\x07'
PASSIVE = b'\x80'
SAFE = b'\x83'
CLEAN = b'\x87'
BEEP = b'\x8c\x03\x01\x40\x10\x8d\x03'



   

def init():
    try:
        print("init roomba")
        print("writing reset")
        ser.write(RESET)
        time.sleep(16)
        print("writing passive")
        ser.write(PASSIVE)
        time.sleep(0.1)
        print("writing safe")
        ser.write(SAFE)
        time.sleep(0.1)
        print("sending 3 beeps to roomba")
        print("writing beeps")
        ser.write(BEEP)
        time.sleep(0.7)
        ser.write(BEEP)
        time.sleep(0.7)
        ser.write(BEEP)
    except Exception as e:
        print("serial error 2", e)

    
def readAll():
    print("read all")
    while True:
        sys.stdout.write(str(ser.read()))
        sys.stdout.flush()


        
if __name__ == "__main__":
    init()
    _thread.start_new_thread(readAll, ())
    while True:
        time.sleep(1)


