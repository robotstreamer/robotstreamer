import subprocess
import shlex
import re
import os
import time
import urllib.request
import platform
import json
import sys
import base64
import random
import argparse

print("example:")
print('python robotstreamer/old_send_video.py 199 0 --screen-capture --kbps 2500 --audio-input-device "Microphone (HD Webcam C270)"')

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
print("args", args)
server = "robotstreamer.com"
cameraID = args.camera_id


def onHandleCameraCommand(*args):
    print(args)


def randomSleep():
    """A short wait is good for quick recovery, but sometimes a longer delay is needed or it will just keep trying and failing short intervals, like because the system thinks the port is still in use and every retry makes the system think it's still in use. So, this has a high likelihood of picking a short interval, but will pick a long one sometimes."""

    timeToWait = random.choice((0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 5))
    print("sleeping", timeToWait)
    time.sleep(timeToWait)



def getVideoPort():

    url = 'http://%s:6001/get_video_port/%s' % (server, cameraID)

    for retryNumber in range(2000):
        try:
            print("GET", url)
            response = urllib.request.urlopen(url).read()
            break
        except:
            print("could not open url ", url)
            time.sleep(2)

    return json.loads(response)['mpeg_stream_port']


def getAudioPort():

    url = 'http://%s:6001/get_audio_port/%s' % (server, cameraID)

    for retryNumber in range(2000):
        try:
            print("GET", url)
            response = urllib.request.urlopen(url).read()
            break
        except:
            print("could not open url ", url)
            time.sleep(2)

    return json.loads(response)['audio_stream_port']



def runFfmpeg(commandLine):

    print(commandLine)
    splitCommandLine = shlex.split(commandLine)
    print("split command line:", splitCommandLine)
    ffmpegProcess = subprocess.Popen(splitCommandLine)
    print("command started")

    return ffmpegProcess




def macVideoCapture(videoPort):

    videoCommandLine = 'ffmpeg -f avfoundation -i 1:none -f mpegts -codec:v mpeg1video -s 640x480 -b:v %dk -bf 0 -muxdelay 0.001 http://%s:%s/hellobluecat/640/480/' % (args.kbps, server, videoPort)
    print("video command line:", videoCommandLine)
    videoProcess = runFfmpeg(videoCommandLine)
    return videoProcess



def macAudioCapture(audioPort):

    audioCommandLine = 'ffmpeg -f avfoundation -i none:0 -f mpegts -codec:a mp2 -b:a 32k -muxdelay 0.001 http://%s:%s/hellobluecat/640/480/' % (server, audioPort)
    print("audio command line:", audioCommandLine)
    audioProcess = runFfmpeg(audioCommandLine)
    return audioProcess



def startVideoCapture():

    videoPort = getVideoPort()
    print("video port:", videoPort)
    videoProcess = macVideoCapture(videoPort)
    return videoProcess



def startAudioCapture():

    audioPort = getAudioPort()
    print("audio port:", audioPort)
    audioProcess = macAudioCapture(audioPort)
    return audioProcess


def timeInMilliseconds():
    return int(round(time.time() * 1000))



def main():

    # clean up, kill any ffmpeg process that are hanging around from a previous run
    print("killing all ffmpeg processes")
    os.system("killall ffmpeg")

    print("main")

    streamProcessDict = None

    twitterSnapCount = 0

    videoProcess = startVideoCapture()
    audioProcess = startAudioCapture()

    while True:
        print("audioProcess.poll()", audioProcess.poll())
        print("videoProcess.poll()", videoProcess.poll())
        time.sleep(1)


if __name__ == "__main__":

    main()
