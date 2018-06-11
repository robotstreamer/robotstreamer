import serial
import time
import _thread
import sys


def handleCommand(command, keyPosition):

    print("handling command")
    
    if command == 'L':
        move(0, 100, 0xFF, negative(100))        
    elif command == 'R':
        move(0, 0, 0, 100)
    elif command == 'F':
        move(0, 100, 0, 100)
    elif command == 'B':
        move(0xFF, negative(100), 0xFF, negative(100))



ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200)

PASSIVE = '\x80'
SAFE = '\x83'
CLEAN = '\x87'
BEEP = '\x8c\x03\x01\x40\x10\x8d\x03'


#time.sleep(1)
#ser.close()

def init():
    print("init roomba")
    for i in range(0, 10):
        serialWrite(PASSIVE)
    serialWrite(SAFE)
    print("sending beep to roomba")
    serialWrite(BEEP)

    
def serialWrite(s):
    ser.write(s.encode())

    
def negative(x):
    return 256 - x


def readAll():
    print("read all")
    while True:
        sys.stdout.write(ser.read())
        sys.stdout.flush()


def move(motorAHigh, motorALow, motorBHigh, motorBLow):
    print("move", motorAHigh, motorALow, motorBHigh, motorBLow)
    serialWrite(chr(146) + chr(motorAHigh) + chr(motorALow) + chr(motorBHigh) + chr(motorBLow))
    time.sleep(0.3)
    serialWrite(chr(146) + chr(0) + chr(0) + chr(0) + chr(0))


def inputFromKeyboard():

    while True:
        data = input("PROMPT>")
        if data == "beep":
            serialWrite(BEEP)
        elif data == 'l':
            move(0, 100, 0, 0)        
        elif data == 'r':
            move(0, 0, 0, 100)
        elif data == 'f':
            move(0, 100, 0, 100)
        elif data == 'b':
            move(0xFF, negative(100), 0xFF, negative(100))
        elif data == 's': #stop
            move(0, 0, 0, 0)
        else:
            print("data:", data)
            num = int(data, 10)
            print("num", num, "end")
            c = chr(num)
            print("char", c, "end")
            serialWrite(c)
        ser.flush()


        
if __name__ == "__main__":
    _thread.start_new_thread(readAll, ())
    inputFromKeyboard()
