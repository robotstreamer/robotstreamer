import serial
import time
import thread
import sys


ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
#ser = serial.Serial(port='/dev/ttyUSB0', baudrate=19200)

#data = '\x83'
#data = '\x87'
beepCode = '\x8c\x03\x01\x40\x10\x8d\x03'
#data = ''

#ser.write(data)

#time.sleep(1)
#ser.close()


def readAll():
    print "read all"
    while True:
        sys.stdout.write(ser.read())
        sys.stdout.flush()

        
thread.start_new_thread(readAll, ())

while True:
    data = raw_input("PROMPT>")
    if data == "beep":
        ser.write(beepCode)
    elif data == 'l':
        ser.write(chr(146) + chr(0) + chr(100) + chr(0) + chr(0))        
        time.sleep(0.3)
        ser.write(chr(146) + chr(0) + chr(0) + chr(0) + chr(0))        
    elif data == 'r':
        ser.write(chr(146) + chr(0) + chr(0) + chr(0) + chr(100))
        time.sleep(0.3)
        ser.write(chr(146) + chr(0) + chr(0) + chr(0) + chr(0))        
    elif data == 'f':
        ser.write(chr(146) + chr(0) + chr(100) + chr(0) + chr(100))
        time.sleep(0.3)
        ser.write(chr(146) + chr(0) + chr(0) + chr(0) + chr(0))        
    elif data == 'b':
        ser.write(chr(146) + chr(255) + chr(100) + chr(255) + chr(100))
        time.sleep(0.3)
        ser.write(chr(146) + chr(0) + chr(0) + chr(0) + chr(0))        
    elif data == 's': #stop
        ser.write(chr(137) + chr(0) + chr(0) + chr(1) + chr(1))
    else:
        print "data:", data
        num = int(data, 10)
        print "num", num, "end"
        c = chr(num)
        print "char", c, "end"
        ser.write(c)
    ser.flush()

        
        
