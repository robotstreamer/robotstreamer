import subprocess
import re

def getAudioPlayingDeviceByName(name):
        return getAudioDeviceByName('aplay', name)

def getAudioRecordingDeviceByName(name):
        return getAudioDeviceByName('arecord', name)

def getAudioDeviceByName(command, name):

        text = subprocess.check_output([command, '-l'])
        lines = text.splitlines()
        for line in lines:
                line = line.decode("utf-8")
                if name in line:
                        print(line)
                        result = re.match("card (.*?):", line)
                        print(result.group(0))
                        print(result.group(1))
                        return int(result.group(1))



if __name__ == "__main__":
        print("as a test, checking for Yeti mic")
        print(getAudioRecordingDeviceByName("Yeti"))
        print("as a test, checking for C920 mic")
        print(getAudioRecordingDeviceByName("C920_1 [HD Pro Webcam C920]"))

