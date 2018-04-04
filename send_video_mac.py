import subprocess
import shlex
import re
import os
import time
import urllib2
import platform
import json
import sys
import base64
import random


import argparse


print "example:"
print 'python robotstreamer/old_send_video.py 199 0 --screen-capture --kbps 2500 --audio-input-device "Microphone (HD Webcam C270)"'

parser = argparse.ArgumentParser(description='robot control')
parser.add_argument('camera_id')
parser.add_argument('video_device_number', default=0, type=int)
parser.add_argument('--kbps', default=2500, type=int)
parser.add_argument('--brightness', type=int, help='camera brightness')
parser.add_argument('--contrast', type=int, help='camera contrast')
parser.add_argument('--saturation', type=int, help='camera saturation')
parser.add_argument('--rotate180', default=False, type=bool, help='rotate image 180 degrees')
parser.add_argument('--env', default="prod")
parser.add_argument('--screen-capture', dest='screen_capture', action='store_true') # tells windows to pull from different camera, this should just be replaced with a video input device option
parser.set_defaults(screen_capture=False)

parser.add_argument('--no-mic', dest='mic', action='store_false')
parser.set_defaults(mic=True)

parser.add_argument('--mic-channels', type=int, help='microphone channels, typically 1 or 2', default=1)

parser.add_argument('--audio-input-device', default='Microphone (HD Webcam C270)') # currently, this option is only used for windows screen capture


args = parser.parse_args()

print "args", args

server = "robotstreamer.com"


from socketIO_client import SocketIO, LoggingNamespace


if args.env == "dev":
    print "using dev port 8122"
    port = 8122
elif args.env == "prod":
    print "using prod port 8022"
    port = 8022
else:
    print "invalid environment"
    sys.exit(0)


print "initializing socket io"
print "server:", server
print "port:", port
#todo: put this back
#socketIO = SocketIO(server, port, LoggingNamespace)
print "finished initializing socket io"

#ffmpeg -f qtkit -i 0 -f mpeg1video -b 400k -r 30 -s 320x240 http://52.8.81.124:8082/hellobluecat/320/240/


def onHandleCameraCommand(*args):
    #thread.start_new_thread(handle_command, args)
    print args

#todo: put this back
#socketIO.on('command_to_camera', onHandleCameraCommand)


def onHandleTakeSnapshotCommand(*args):
    print "taking snapshot"
    inputDeviceID = streamProcessDict['device_answer']
    snapShot(platform.system(), inputDeviceID)
    with open ("snapshot.jpg", 'rb') as f:
        data = f.read()
    print "emit"

    socketIO.emit('snapshot', {'image':base64.b64encode(data)})

#todo: put this back
#socketIO.on('take_snapshot_command', onHandleTakeSnapshotCommand)


def randomSleep():
    """A short wait is good for quick recovery, but sometimes a longer delay is needed or it will just keep trying and failing short intervals, like because the system thinks the port is still in use and every retry makes the system think it's still in use. So, this has a high likelihood of picking a short interval, but will pick a long one sometimes."""

    timeToWait = random.choice((0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 5))
    print "sleeping", timeToWait
    time.sleep(timeToWait)



def getVideoPort():


    url = 'http://%s:6001/get_video_port/%s' % (server, cameraIDAnswer)


    for retryNumber in range(2000):
        try:
            print "GET", url
            response = urllib2.urlopen(url).read()
            break
        except:
            print "could not open url ", url
            time.sleep(2)

    return json.loads(response)['mpeg_stream_port']

def getAudioPort():


    url = 'http://%s:6001/get_audio_port/%s' % (server, cameraIDAnswer)


    for retryNumber in range(2000):
        try:
            print "GET", url
            response = urllib2.urlopen(url).read()
            break
        except:
            print "could not open url ", url
            time.sleep(2)

    return json.loads(response)['audio_stream_port']



def runFfmpeg(commandLine):

    print commandLine
    ffmpegProcess = subprocess.Popen(shlex.split(commandLine))
    print "command started"

    return ffmpegProcess






def handleMacScreenCapture(deviceNumber, videoPort, audioPort):

    videoCommandLine = 'ffmpeg -f avfoundation -i 1:none -f mpegts -codec:v mpeg1video -s 640x480 -b:v %dk -bf 0 -muxdelay 0.001 http://%s:%s/hellobluecat/640/480/' % (args.kbps, server, videoPort)
    audioCommandLine = 'ffmpeg -f avfoundation -i none:0 -f mpegts -codec:a mp2 -b:a 32k -muxdelay 0.001 http://%s:%s/hellobluecat/640/480/' % (server, audioPort)

    print "video command line:", videoCommandLine
    print "audio command line:", audioCommandLine

    #videoProcess = runFfmpeg(videoCommandLine)
    audioProcess = runFfmpeg(audioCommandLine)




def startVideoCapture():

    videoPort = getVideoPort()
    audioPort = getAudioPort()
    print "video port:", videoPort
    print "audio port:", audioPort

    deviceNumber = args.video_device_number

    result = None

    result = handleMacScreenCapture(deviceNumber, videoPort, audioPort)

    return result


def timeInMilliseconds():
    return int(round(time.time() * 1000))



def main():

    # clean up, kill any ffmpeg process that are hanging around from a previous run
    print "killing all ffmpeg processes"
    os.system("killall ffmpeg")

    print "main"

    streamProcessDict = None

    twitterSnapCount = 0

    startVideoCapture()

    while True:
        print "monitor"
        time.sleep(1)



if __name__ == "__main__":


    #if len(sys.argv) > 1:
    #    cameraIDAnswer = sys.argv[1]
    #else:
    #    cameraIDAnswer = raw_input("Enter the Camera ID for your robot, you can get it by pointing a browser to the robotstreamer server %s: " % server)

    cameraIDAnswer = args.camera_id


    main()
