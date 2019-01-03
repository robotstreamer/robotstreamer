import subprocess
import shlex
import re
import os
import time
import platform
import json
import sys
import base64
import random
import datetime
import traceback
import robot_util
import _thread
import copy
import argparse
import audio_util
import urllib.request
from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue
#from Queue import Queue # Python 2

parser = argparse.ArgumentParser(description='robot control')
parser.add_argument('camera_id')


parser.add_argument('--api-server', help="Server that robot will connect to listen for API update events", default='http://api.robotstreamer.com:8080')
parser.add_argument('--env', default="prod")
parser.add_argument('--stream-key', default='hellobluecat')


commandArgs = parser.parse_args()
apiServer = commandArgs.api_server

#from socketIO_client import SocketIO, LoggingNamespace

def main():

    global robotID
    global audioProcess
    global videoProcess


    robot_util.sendCameraAliveMessage(apiServer, commandArgs.camera_id)

    count = 0

    while True:
        
        time.sleep(1)
        if (count % robot_util.KeepAlivePeriod) == 0:
            print("sending camera alive message")
            robot_util.sendCameraAliveMessage(apiServer,
                                              commandArgs.camera_id)

        count += 1


main()
