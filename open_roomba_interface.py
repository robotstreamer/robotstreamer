import serial
import time
import _thread
import sys
import robot_util


try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
except Exception as e:
    print(e)
#ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200)

PASSIVE = b'\x80'
SAFE = b'\x83'
CLEAN = b'\x87'
BEEP = b'\x8c\x03\x01\x40\x10\x8d\x03'

movementSystemActive = False



def handleCommand(command, keyPosition):

    global lastCommand

    print("handling command")

    if command == 'L':
        move(100, -100, 0, .20, 0)
    elif command == 'R':
        move(-100, 100, 0, .20, 0)
    elif command == 'F':
        move(100, 100, .09, .40, .18)
    elif command == 'B':
        move(-100, -100, .09, .40, .18)

    robot_util.handleSoundCommand(command, keyPosition)

    

def init():
    try:
        print("init roomba")
        ser.write(PASSIVE)
        ser.write(SAFE)
        print("sending beep to roomba")
        ser.write(BEEP)
    except:
        print("died")

    
#def serialWrite(s):
#    ser.write(s.encode())

    
def negative(x):
    return 256 - x


def readAll():
    print("read all")
    while True:
        sys.stdout.write(ser.read())
        sys.stdout.flush()

def twosComp(x):
    if x < 0:
        return negative(-x)
    return x
        

def move(motorA, motorB, rampUpTime, fullSpeedTime, rampDownTime):

    global movementSystemActive
    
    motorA1 = twosComp(motorA)
    motorA2 = twosComp(int(motorA / 3))
    motorB1 = twosComp(motorB)
    motorB2 = twosComp(int(motorB / 3))

    # set high bytes
    if motorA < 0:
        highA = 0xFF
    else:
        highA = 0
    if motorB < 0:
        highB = 0xFF
    else:
        highB = 0
        

    if not movementSystemActive:
        movementSystemActive = True

        # ramp up
        rawMove(highA, motorA2, highB, motorB2)
        time.sleep(rampUpTime)

        # move full speed
        rawMove(highA, motorA1, highB, motorB1)
        time.sleep(fullSpeedTime)

        # ramp down
        rawMove(highA, motorA2, highB, motorB2)
        time.sleep(rampDownTime)

        # stop
        rawMove(0, 0, 0, 0)
        
        movementSystemActive = False

        
def rawMove(motorAHigh, motorALow, motorBHigh, motorBLow):


    
    print("raw move", motorAHigh, motorALow, motorBHigh, motorBLow)
    #ser.write(bytes([128,128])
    #ser.write(bytes([131])
    ser.write(bytes([128]))
    ser.write(bytes([131]))
    ser.write(bytes([146, motorAHigh, motorALow, motorBHigh, motorBLow]))



def inputFromKeyboard():

    while True:
        data = input("PROMPT>")
        if data == "beep":
            ser.write(BEEP)
        elif data == 'l':
            move(100, -100, .05, .2, .25)
        elif data == 'r':
            move(-100, 100, .05, .2, .25)
        elif data == 'f':
            move(100, 100, .05, .2, .25)
        elif data == 'b':
            move(-100, -100, .05, .2, .25)
        elif data == 's': #stop
            move(0, 0, 0, 0, .05, .2, .25)
        else:
            print("data:", data)
            num = int(data, 10)
            print("num", num, "end")
            c = chr(num)
            print("char", c, "end")
            #ser.write(c)
            ser.write(bytes([num]))
        ser.flush()


        
if __name__ == "__main__":
    _thread.start_new_thread(readAll, ())
    inputFromKeyboard()
