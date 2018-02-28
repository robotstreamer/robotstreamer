import os
import time
import traceback
import ssl
import urllib.request
import getpass
import json



ConfigFilename = "/home/pi/config_" + getpass.getuser() + ".json"



def times(lst, number):
        return [x*number for x in lst]


def getWithRetry(url, secure=True):

    for retryNumber in range(2000):
        try:
            print("GET", url)
            if secure:
                response = urllib.request.urlopen(url).read()
            else:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(url, context=ctx).read()
            break
        except:
            print("could not open url", url)
            traceback.print_exc()
            time.sleep(2)

    return response



def sendSerialCommand(ser, command):


    print(ser.name)         # check which port was really used
    ser.nonblocking()

    # loop to collect input
    #s = "f"
    #print "string:", s
    print(str(command.lower()))
    ser.write(command.lower() + "\r\n")     # write a string
    #ser.write(s)
    ser.flush()

    #while ser.in_waiting > 0:
    #    print "read:", ser.read()

    #ser.close()



