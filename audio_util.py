import subprocess
import requests
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
                print(name, line)
                if name in line:
                        print(line)
                        result = re.match("card (.*?):", line)
                        print(result.group(0))
                        print(result.group(1))
                        return int(result.group(1))


def postToLocalSpeechService(text, cardNumber):
    url = 'http://127.0.0.1:5000/speak'
    json_data = {'text': text, 'card_number': cardNumber}
    response = requests.post(url, json=json_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")


    
if __name__ == "__main__":
        print("as a test, checking for Yeti mic")
        print(getAudioRecordingDeviceByName("Yeti"))
        print("as a test, checking for C920 mic")
        print(getAudioRecordingDeviceByName("C920_1 [HD Pro Webcam C920]"))
        print("as a test, checking for USB2.0 Device (the usb speaker)")
        print(getAudioPlayingDeviceByName("USB2.0 Device"))

