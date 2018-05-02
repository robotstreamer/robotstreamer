import os
import asyncio
import websockets
import time
import argparse
import json
import robot_util
import _thread
import traceback
import tempfile
import uuid
import audio



apiHost = "robotstreamer.com:6001"
controlHost = "robotstreamer.com"
chatHostPort = {"host":"184.72.15.121", "port":8765}
allowedVoices = ['en-us', 'af', 'bs', 'da', 'de', 'el', 'eo', 'es', 'es-la', 'fi', 'fr', 'hr', 'hu', 'it', 'kn', 'ku', 'lv', 'nl', 'pl', 'pt', 'pt-pt', 'ro', 'sk', 'sr', 'sv', 'sw', 'ta', 'tr', 'zh', 'ru']
tempDir = tempfile.gettempdir()
print("temporary directory:", tempDir)


parser = argparse.ArgumentParser(description='start robot control program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--forward', default='[-1,1,-1,1]')
parser.add_argument('--left', default='[1,1,1,1]')
parser.add_argument('--no-secure-cert', dest='secure_cert', action='store_false')
parser.add_argument('--voice-number', type=int, default=1)
parser.add_argument('--male', dest='male', action='store_true')
parser.add_argument('--festival-tts', dest='festival_tts', action='store_true')
parser.add_argument('--enable-ping-pong', dest='enable_ping_pong', action='store_true')
parser.set_defaults(enable_ping_pong=False)
parser.add_argument('--tts-volume', type=int, default=80)
parser.add_argument('--type', default="rsbot")



commandArgs = parser.parse_args()

print(commandArgs)


if commandArgs.type == "rsbot":
            print("initializing rsbot")
            import rsbot_interface as interface
            interface.init(json.loads(commandArgs.forward),
                              json.loads(commandArgs.left),
                              commandArgs.enable_ping_pong)
elif commandArgs.type == "windows_interface":
            import windows_interface as interface

elif commandArgs.type == "gopigo3":
            import gopigo3_interface as interface

elif commandArgs.type == "gopigo":
            import gopigo_interface as interface
            

            


# set volume level

# tested for 3.5mm audio jack
#os.system("amixer set PCM -- 100%d%%" % commandArgs.tts_volume)
#if commandArgs.tts_volume > 50:
    #os.system("amixer set PCM -- -100")


def setVolume(percent):
            print("setting volume to", percent, "%")
            for cardNumber in range(0, 5):
                        for numid in range(0,5):
                                    os.system("amixer -c %d cset numid=%d %d%%" % (cardNumber, numid, percent))
            

def espeak(hardwareNumber, message, voice):

            # tested for USB audio device
            #os.system("amixer -c 2 cset numid=%d %d%%" %
            #          (hardwareNumber, commandArgs.tts_volume))
            
            tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
            f = open(tempFilePath, "w")
            f.write(message)
            f.close()
            
            print('plughw:%d,0' % hardwareNumber)
            if commandArgs.male:
                os.system('cat ' + tempFilePath + ' | espeak -v%s --stdout | aplay -D plughw:%d,0' % (voice, hardwareNumber))
            else:
                os.system('cat ' + tempFilePath + ' | espeak -v%s+f%d -s170 --stdout | aplay -D plughw:%d,0' % (voice, commandArgs.voice_number, hardwareNumber))


            os.remove(tempFilePath)



def espeakMac(message, voice):

            # tested for USB audio device
            #os.system("amixer -c 2 cset numid=%d %d%%" %
            #          (hardwareNumber, commandArgs.tts_volume))
            
            tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
            f = open(tempFilePath, "w")
            f.write(message)
            f.close()
            
            os.system('cat ' + tempFilePath + ' | espeak')

            os.remove(tempFilePath)
                



def say(message, voice='en-us'):

    os.system("killall espeak")
    
    if voice not in allowedVoices:
        print("invalid voice")
        return
    
    tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
    f = open(tempFilePath, "w")
    f.write(message)
    f.close()


    #os.system('"C:\Program Files\Jampal\ptts.vbs" -u ' + tempFilePath) Whaa?
    
    if commandArgs.festival_tts:
        # festival tts
        os.system('festival --tts < ' + tempFilePath)
    #os.system('espeak < /tmp/speech.txt')

    else:
        # espeak tts
        #todo: these could be defined in the interface modules perhaps

        if commandArgs.type == "mac":
                _thread.start_new_thread(espeakMac, (message, voice))

        else:
            for hardwareNumber in (0, 2, 3, 1, 4):
                #_thread.start_new_thread(espeak, (hardwareNumber, message, voice))
                espeak(hardwareNumber, message, voice)


    os.remove(tempFilePath)



def getControlHostPort():

        url = 'http://%s/get_control_host_port/%s' % (apiHost, commandArgs.robot_id)
        response = robot_util.getWithRetry(url, secure=commandArgs.secure_cert)
        print("response:", response)
        return json.loads(response)
            

async def handleControlMessages():

    port = getControlHostPort()['port']
    print("connecting to port:", port)
    url = 'ws://%s:%s/echo' % (controlHost, port)

    async with websockets.connect(url) as websocket:

        print("connected to control service at", url)
        print("control websocket object:", websocket)
        
        while True:

            print("awaiting control message")
            
            message = await websocket.recv()
            print("< {}".format(message))
            j = json.loads(message)
            print(j)
            _thread.start_new_thread(interface.handleCommand, (j["command"],
                                                               j["key_position"]))


            
async def handleChatMessages():

    url = 'ws://%s:%s' % (chatHostPort['host'], chatHostPort['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        print("connected to control service at", url)
        print("chat websocket object:", websocket)

        #todo: you do need this as an connection initializer, but you should make the server not need it
        await websocket.send(json.dumps({"message":"message"}))     

        while True:

            print("awaiting chat message")
            
            message = await websocket.recv()
            print("< {}".format(message))
            j = json.loads(message)
            print("message:", j)
            if ('message' in j) and ('tts' in j) and j['tts'] == True and (j['robot_id'] == commandArgs.robot_id):
                        if audio.espeakBytes(j['message']) < 400000:
                                    print("length", audio.espeakBytes(j['message']))
                                    _thread.start_new_thread(say, (j['message'],))
                        else:
                                    print("message too long")
            else:
                print("error, message not valid:", j)

            

            
def startControl():
    print("waiting a few seconds")
    time.sleep(6) #todo: only wait as needed (wait for interent)

    while True:
                print("starting stat control loop")
                time.sleep(0.25)
                try:
                            asyncio.new_event_loop().run_until_complete(handleControlMessages())
                except:
                            print("error")
                            traceback.print_exc()
                print("control died")
                interface.movementSystemActive = False


def startChat():
        time.sleep(10) #todo: only wait as needed (wait for interenet)
        print("restarting loop")
        time.sleep(0.25)
        try:
                asyncio.new_event_loop().run_until_complete(handleChatMessages())
        except:
                print("error")
                traceback.print_exc()


#async def hello(uri):
#       async with websockets.connect(uri) as websocket:
#                await websocket.send(json.dumps({"message":"message"}))
#                while True:
#                        print("recv")
#                        x = await websocket.recv()
#                        print(x)

#def startTest():
#        asyncio.get_event_loop().run_until_complete(
#                hello('ws://54.219.138.36:8765'))
        
def main():                

                       
            print(commandArgs)
            
            _thread.start_new_thread(startControl, ())
            _thread.start_new_thread(startChat, ())
            #_thread.start_new_thread(startTest, ())
            #startTest()

            setVolume(commandArgs.tts_volume)
            
            
            while True:
                time.sleep(1)


                
if __name__ == '__main__':
    main()


