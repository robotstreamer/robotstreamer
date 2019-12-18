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
from usb.core import find as finddev

class DummyProcess:
    def poll(self):
        return None
    def __init__(self):
        self.pid = 123456789


parser = argparse.ArgumentParser(description='robot control')
parser.add_argument('camera_id')
parser.add_argument('video_device_number', default=0, type=int)


parser.add_argument('--api-url', help="Server that robot will connect to listen for API update events", default='http://api.robotstreamer.com:8080')
parser.add_argument('--xres', type=int, default=768)
parser.add_argument('--yres', type=int, default=432)
parser.add_argument('--audio-device-number', default=1, type=int)
parser.add_argument('--audio-device-name')
parser.add_argument('--audio-rate', default=48000, type=int, help="this is 44100 or 48000 usually")
parser.add_argument('--kbps', default=350, type=int)
parser.add_argument('--brightness', type=int, help='camera brightness')
parser.add_argument('--contrast', type=int, help='camera contrast')
parser.add_argument('--saturation', type=int, help='camera saturation')
parser.add_argument('--rotate180', default=False, type=bool, help='rotate image 180 degrees')
parser.add_argument('--env', default="prod")
parser.add_argument('--screen-capture', dest='screen_capture', action='store_true') # tells windows to pull from different camera, this should just be replaced with a video input device option
parser.set_defaults(screen_capture=False)
parser.add_argument('--no-mic', dest='mic_enabled', action='store_false')
parser.set_defaults(mic_enabled=True)
parser.add_argument('--no-restart-on-video-fail', dest='restart_on_video_fail', action='store_false')
parser.set_defaults(restart_on_video_fail=True)
parser.add_argument('--no-audio-restart', dest='audio_restart_enabled', action='store_false')
parser.set_defaults(audio_restart_enabled=True)
parser.add_argument('--no-camera', dest='camera_enabled', action='store_false')
parser.set_defaults(camera_enabled=True)
parser.add_argument('--dry-run', dest='dry_run', action='store_true')
parser.add_argument('--mic-channels', type=int, help='microphone channels, typically 1 or 2', default=1)
parser.add_argument('--audio-input-device', default='Microphone (HD Webcam C270)') # currently, this option is only used for windows screen capture
parser.add_argument('--stream-key', default='hellobluecat')
parser.add_argument('--ffmpeg-path', default='/usr/local/bin/ffmpeg')
parser.add_argument('--usb-reset-id', default=None)

charCount = {}
lastCharCount = None
commandArgs = parser.parse_args()
robotSettings = None
resolutionChanged = False
currentXres = None
currentYres = None
apiServer = commandArgs.api_url

audioProcess = None
videoProcess = None

#from socketIO_client import SocketIO, LoggingNamespace

# enable raspicam driver in case a raspicam is being used
os.system("sudo modprobe bcm2835-v4l2")




def reader(pipe, queue):
    try:
        with pipe:
            #for line in iter(pipe.readline, b''):
            #    queue.put((pipe, line))
            while True:
                c = pipe.read(1)
                if not c:
                    print("End of file")
                    break
                #print("Read a character:", c)
                queue.put((pipe, c))
                
    finally:
        queue.put(None)

        

def printOutput(label, q):

    global charCount
    charCount[label] = 0
    for _ in range(2):
        for source, line in iter(q.get, None):
            print(line.decode("utf-8"), end="")
            charCount[label] += 1
            #print(label + "(" + str(charCount[label]) + ")", end="")
            #print("%s %s: %s" % (label, source, line))

            
    
def runAndMonitor(label, command):
    process = Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1)
    q = Queue()
    Thread(target=reader, args=[process.stdout, q]).start()
    Thread(target=reader, args=[process.stderr, q]).start()
    Thread(target=printOutput, args=[label, q]).start()
    return process

def getVideoEndpoint():
    url = '%s/v1/get_endpoint/jsmpeg_video_capture/%s' % (apiServer, commandArgs.camera_id)
    response = robot_util.getWithRetry(url)
    return json.loads(response)

def getAudioEndpoint():
    url = '%s/v1/get_endpoint/jsmpeg_audio_capture/%s' % (apiServer, commandArgs.camera_id)
    response = robot_util.getWithRetry(url)
    return json.loads(response)

def getOnlineRobotSettings(robotID):
    url = '%s/api/v1/robots/%s' % (apiServer, robotID)
    response = robot_util.getWithRetry(url)
    return json.loads(response)

def randomSleep():
    """A short wait is good for quick recovery, but sometimes a longer delay is needed or it will just keep 
    trying and failing short intervals, like because the system thinks the port is still in use and every retry 
    makes the system think it's still in use. So, this has a high likelihood of picking a short interval, 
    but will pick a long one sometimes."""

    timeToWait = random.choice((0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1))
    t = timeToWait * 12.0
    print("sleeping", t, "seconds")
    time.sleep(t)



def startVideoCaptureLinux():

    videoEndpoint = getVideoEndpoint()
    videoHost = videoEndpoint['host']
    videoPort = videoEndpoint['port']

    print("start video capture, video endpoint:", videoEndpoint)


    # set brightness
    if (robotSettings.brightness is not None):
        print("brightness")
        os.system("v4l2-ctl -c brightness={brightness}".format(brightness=robotSettings.brightness))

    # set contrast
    if (robotSettings.contrast is not None):
        print("contrast")
        os.system("v4l2-ctl -c contrast={contrast}".format(contrast=robotSettings.contrast))

    # set saturation
    if (robotSettings.saturation is not None):
        print("saturation")
        os.system("v4l2-ctl -c saturation={saturation}".format(saturation=robotSettings.saturation))


    videoCommandLine = '{ffmpeg_path} -f v4l2 -framerate 25 -video_size {xres}x{yres} -r 25 -i /dev/video{video_device_number} {rotation_option} \
                        -f mpegts -codec:v mpeg1video -b:v {kbps}k -bf 0 -muxdelay 0.001 http://{video_host}:{video_port}/{stream_key}/{xres}/{yres}/'\
                        .format(ffmpeg_path=robotSettings.ffmpeg_path, video_device_number=robotSettings.video_device_number, rotation_option=rotationOption(),\
                        kbps=robotSettings.kbps, video_host=videoHost, video_port=videoPort, xres=robotSettings.xres, yres=robotSettings.yres, stream_key=robotSettings.stream_key)
    
    print(videoCommandLine)

    #return subprocess.Popen(shlex.split(videoCommandLine))
    return runAndMonitor("video", shlex.split(videoCommandLine))



def startAudioCaptureLinux():


    audioEndpoint = getAudioEndpoint()
    audioHost = audioEndpoint['host']
    audioPort = audioEndpoint['port']

    audioDevNum = robotSettings.audio_device_number
    if robotSettings.audio_device_name is not None:
        audioDevNum = audio_util.getAudioDeviceByName(robotSettings.audio_device_name)

    #audioCommandLine = '%s -f alsa -ar 44100 -ac %d -i hw:%d -f mpegts -codec:a mp2 -b:a 32k -muxdelay 0.001 http://%s:%s/%s/640/480/' % (robotSettings.ffmpeg_path, robotSettings.mic_channels, audioDevNum, audioHost, audioEndpoint['port'], robotSettings.stream_key)
    audioCommandLine = '%s -f alsa -ar %d -ac %d -i hw:%d -f mpegts -codec:a mp2 -b:a 64k -muxdelay 0.01 http://%s:%s/%s/640/480/'\
                        % (robotSettings.ffmpeg_path, robotSettings.audio_rate, robotSettings.mic_channels, audioDevNum, audioHost, audioPort, robotSettings.stream_key)
    print(audioCommandLine)
    if commandArgs.usb_reset_id != None:
      if len(commandArgs.usb_reset_id) == 8:
        vendor_id=int(commandArgs.usb_reset_id[0:4], 16)
        product_id=int(commandArgs.usb_reset_id[4:], 16)
        dev=finddev(idVendor=vendor_id, idProduct=product_id)
        dev.reset()
    #return subprocess.Popen(shlex.split(audioCommandLine))
    return runAndMonitor("audio", shlex.split(audioCommandLine))



def rotationOption():

    if robotSettings.rotate180:
        return "-vf transpose=2,transpose=2"
    else:
        return ""


def onCommandToRobot(*args):
    global robotID

    if len(args) > 0 and 'robot_id' in args[0] and args[0]['robot_id'] == robotID:
        commandMessage = args[0]
        print('command for this robot received:', commandMessage)
        command = commandMessage['command']

        if command == 'VIDOFF':
            print('disabling camera capture process')
            print("args", args)
            robotSettings.camera_enabled = False
            os.system("killall ffmpeg")

        if command == 'VIDON':
            if robotSettings.camera_enabled:
                print('enabling camera capture process')
                print("args", args)
                robotSettings.camera_enabled = True

        sys.stdout.flush()


def onConnection(*args):
    print('connection:', args)
    sys.stdout.flush()


def onRobotSettingsChanged(*args):
    print('---------------------------------------')
    print('set message recieved:', args)
    refreshFromOnlineSettings()



def killallFFMPEGIn30Seconds():
    time.sleep(30)
    os.system("killall ffmpeg")



#todo, this needs to work differently. likely the configuration will be json and pull in stuff from command line rather than the other way around.
def overrideSettings(commandArgs, onlineSettings):
    global resolutionChanged
    global currentXres
    global currentYres
    resolutionChanged = False
    c = copy.deepcopy(commandArgs)
    print("onlineSettings:", onlineSettings)
    if 'mic_enabled' in onlineSettings:
        c.mic_enabled = onlineSettings['mic_enabled']
    if 'xres' in onlineSettings:
        if currentXres != onlineSettings['xres']:
            resolutionChanged = True
        c.xres = onlineSettings['xres']
        currentXres = onlineSettings['xres']
    if 'yres' in onlineSettings:
        if currentYres != onlineSettings['yres']:
            resolutionChanged = True
        c.yres = onlineSettings['yres']
        currentYres = onlineSettings['yres']
    print("onlineSettings['mic_enabled']:", onlineSettings['mic_enabled'])
    return c


def refreshFromOnlineSettings():
    global robotSettings
    global resolutionChanged
    print("refreshing from online settings")
    #onlineSettings = getOnlineRobotSettings(robotID)
    #robotSettings = overrideSettings(commandArgs, onlineSettings)
    robotSettings = commandArgs

    if not robotSettings.mic_enabled:
        print("KILLING**********************")
        if audioProcess is not None:
            print("KILLING**********************")
            audioProcess.kill()

    if resolutionChanged:
        print("KILLING VIDEO DUE TO RESOLUTION CHANGE**********************")
        if videoProcess is not None:
            print("KILLING**********************")
            videoProcess.kill()

    else:
        print("NOT KILLING***********************")


def checkForStuckProcesses():

    global lastCharCount
    if lastCharCount is not None:

        if robotSettings.camera_enabled:
            videoInfoRate = charCount['video'] - lastCharCount['video']
            print("video info rate:", videoInfoRate)
            if abs(videoInfoRate) < 10:
                print("video process has stopped outputting info")
                print("KILLING VIDEO PROCESS")
                videoProcess.kill()

        if robotSettings.mic_enabled:
            audioInfoRate = charCount['audio'] - lastCharCount['audio']
            print("audio info rate:", audioInfoRate)
            if abs(audioInfoRate) < 10:
                print("audio process has stopped outputting info")
                print("KILLING AUDIO PROCESS")
                audioProcess.kill()
        


            
    print("ffmpeg output character count:", charCount)
    lastCharCount = copy.deepcopy(charCount)


    

def main():

    global robotID
    global audioProcess
    global videoProcess


    # overrides command line parameters using config file
    print("args on command line:", commandArgs)

    robot_util.sendCameraAliveMessage(apiServer, commandArgs.camera_id, commandArgs.stream_key)
    #starts the backend services and

    print("camera id:", commandArgs.camera_id)

    refreshFromOnlineSettings()

    print("args after loading from server:", robotSettings)

    #todo need to implement for robotstreamer
    # appServerSocketIO.on('command_to_robot', onCommandToRobot)
    # appServerSocketIO.on('connection', onConnection)
    # appServerSocketIO.on('robot_settings_changed', onRobotSettingsChanged)



    sys.stdout.flush()


    if robotSettings.camera_enabled:
        if not commandArgs.dry_run:
            videoProcess = startVideoCaptureLinux()
        else:
            videoProcess = DummyProcess()

    if robotSettings.mic_enabled:
        if not commandArgs.dry_run:
            audioProcess = startAudioCaptureLinux()
            if commandArgs.audio_restart_enabled:
                _thread.start_new_thread(killallFFMPEGIn30Seconds, ())
            #appServerSocketIO.emit('send_video_process_start_event', {'camera_id': commandArgs.camera_id})
        else:
            audioProcess = DummyProcess()


    numVideoRestarts = 0
    numAudioRestarts = 0

    count = 0


    # loop forever and monitor status of ffmpeg processes
    while True:
        
        print("-----------------" + str(count) + "-----------------")

        #todo: start using this again
        #appServerSocketIO.wait(seconds=1)

        time.sleep(1)



        # todo: note about the following ffmpeg_process_exists is not technically true, but need to update
        # server code to check for send_video_process_exists if you want to set it technically accurate
        # because the process doesn't always exist, like when the relay is not started yet.
        # send status to server
        ######appServerSocketIO.emit('send_video_status', {'send_video_process_exists': True,
        ######                                    'ffmpeg_process_exists': True,
        ######                                    'camera_id':commandArgs.camera_id})




        if numVideoRestarts > 20:
            if commandArgs.restart_on_video_fail:
                print("rebooting in 20 seconds because of too many restarts. probably lost connection to camera")
                time.sleep(20)
                os.system("sudo reboot")

        if count % 20 == 0:
            try:
                with os.fdopen(os.open('/tmp/send_video_summary.txt', os.O_WRONLY | os.O_CREAT, 0o777), 'w') as statusFile:
                    statusFile.write("time" + str(datetime.datetime.now()) + "\n")
                    statusFile.write("video process poll " + str(videoProcess.poll()) + " pid " + str(videoProcess.pid) + " restarts " + str(numVideoRestarts) + " \n")
                    statusFile.write("audio process poll " + str(audioProcess.poll()) + " pid " + str(audioProcess.pid) + " restarts " + str(numAudioRestarts) + " \n")
                print("status file written")
                sys.stdout.flush()
            except:
                print("status file could not be written")
                traceback.print_exc()
                sys.stdout.flush()


        if (count % robot_util.KeepAlivePeriod) == 0:
            print("")
            print("sending camera alive message")
            print("")
            robot_util.sendCameraAliveMessage(apiServer,
                                              commandArgs.camera_id,
                                              robotSettings.stream_key)



        if (count % 2) == 0:
            checkForStuckProcesses()
            
            

        if robotSettings.camera_enabled:

            print("video process poll", videoProcess.poll(), "pid", videoProcess.pid, "restarts", numVideoRestarts)

            # restart video if needed
            if videoProcess.poll() != None:
                randomSleep()
                videoProcess = startVideoCaptureLinux()
                numVideoRestarts += 1
        else:
            print("video process poll: camera_enabled is false")



        if robotSettings.mic_enabled:

            if audioProcess is None:
                print("audio process poll: audioProcess object is None")
            else:
                print("audio process poll", audioProcess.poll(), "pid", audioProcess.pid, "restarts", numAudioRestarts)

            # restart audio if needed
            if (audioProcess is None) or (audioProcess.poll() != None):
                randomSleep()
                audioProcess = startAudioCaptureLinux()
                #time.sleep(30)
                #appServerSocketIO.emit('send_video_process_start_event', {'camera_id': commandArgs.camera_id})
                numAudioRestarts += 1
        else:
            print("audio process poll: mic_enabled is false")


        count += 1


main()
