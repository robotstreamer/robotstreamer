import subprocess
import serial
import time
import _thread
import sys
import robot_util


try:
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=0.03)
except Exception as e:
    print("serial error 1", e)

#ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200)

RESET = b'\x07'
PASSIVE = b'\x80'
SAFE = b'\x83'
CLEAN = b'\x87'
BEEP = b'\x8c\x03\x01\x40\x10\x8d\x03'
VOLTAGE = b'\x8e\x16'
POWER = b'\x85'
LVCO = 11000 #roomba will power down at this battery voltage in mV

movementSystemActive = False

commandArgs = None


def handleCommand(command, keyPosition, price=0):

    global lastCommand

    print("handling command")
    print("keyposition: ", keyPosition)
    print("command: ", command)

    speed = int(commandArgs.straight_speed / 2)

    if command == 'L':
        move(100, -100, 0, .20, 0)
    elif command == 'R':
        move(-100, 100, 0, .20, 0)
    elif command == 'F':
        move(speed, speed, .09, .40, .18)
    elif command == 'B':
        move(-speed, -speed, .09, .40, .18)

    ser.reset_input_buffer()
    ser.write(VOLTAGE)
    ser.flush()
    packet=b''
    packet=ser.read(2)
    if len(packet) == 2:
        voltage=int.from_bytes(packet, 'big')
        print('voltage:', voltage)
        if voltage < LVCO:
            robot_util.aplayFile('/home/pi/sound/recharge.wav')
            ser.write(POWER)
            ser.flush()
            time.sleep(3)
            subprocess.run(['/usr/bin/sudo', '/sbin/shutdown', '-h', 'now' ] )
    robot_util.handleSoundCommand(command, keyPosition, price)

    

def init(cArgs):
    global commandArgs
    commandArgs = cArgs
    try:
        print("init roomba")
        ser.write(RESET)
        time.sleep(0.1)
        #ser.write(PASSIVE)
        #ser.write(SAFE)
        #print("sending 3 beep to roomba")
        #ser.write(BEEP)
        #time.sleep(0.7)
        #ser.write(BEEP)
        #time.sleep(0.7)
        #ser.write(BEEP)
    except Exception as e:
        print("serial error 2", e)

    
#def serialWrite(s):
#    ser.write(s.encode())

    
def negative(x):
    return 256 - x


def readAll():
    print("read all")
    while True:
        sys.stdout.write(str(ser.read()))
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
