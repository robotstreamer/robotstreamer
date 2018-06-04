import serial
import time
import thread


ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

#data = '\x83'
data = '\x87'
#data = '\x8c\x03\x01\x40\x10\x8d\x03'
#data = ''

ser.write(data)

time.sleep(1)
#ser.close()


def readAll():
    print "read all"
    while True:
        print ser.read(),

        
thread.start_new_thread(readAll, ())

while True:
    data = raw_input("PROMPT>")
    print "data:", data
    num = int(data, 16)
    print "num", num, "end"
    c = chr(num)
    print "char", c, "end"
    ser.write(c)
    ser.flush()

        
        
