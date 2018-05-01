#!/bin/python3

#This code was adapted from send_video.py to do the bare minimum to make the
#red "now playing" button turn on. The goal is to allow more flexibility in
#how a user chooses to interface with the robotstreamer. This script requires
#only one parameter the camera id. I recommend that it be called in and killed
#in an automated manner so that the light doesn't get left on by accident after
#the stream is stopped or fails.

import time
import sys
import traceback
import robot_util
import argparse


parser = argparse.ArgumentParser(description='turns the red dot on for your stream')
parser.add_argument('camera_id')
parser.add_argument('--info-server', help="handles things such as rest API requests about ports, for example 1.1.1.1:8082", default='robotstreamer.com:6001')
parser.add_argument('--info-server-protocol', default="http", help="either https or http")
parser.add_argument('--app-server-socketio-host', default="robotstreamer.com", help="wherever app is running")
parser.add_argument('--app-server-socketio-port', default=8022, help="typically use 8022 for prod, 8122 for dev, and 8125 for dev2")
parser.add_argument('--api-server', help="Server that robot will connect to listen for API update events", default='api.robotstreamer.com')

commandArgs = parser.parse_args()
server = 'robotstreamer.com'
infoServer = commandArgs.info_server
apiServer = commandArgs.api_server
infoServerProtocol = commandArgs.info_server_protocol

def main():
    count = 0
    robot_util.sendCameraAliveMessage(infoServerProtocol,
                                      infoServer,
                                      commandArgs.camera_id)

    sys.stdout.flush()

    # loop forever and send keep alive every robot_util.KeepAlivePeriod seconds
    while True:
        time.sleep(1)
        if (count % 5) == 0:
            print( count )
        if (count % robot_util.KeepAlivePeriod) == 0:
            robot_util.sendCameraAliveMessage(infoServerProtocol,
                                              infoServer,
                                              commandArgs.camera_id)


        count += 1


main()
