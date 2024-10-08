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
import datetime
import importlib
import audio_util
try:
    import google_tts
except ImportError:
    print("warning: google tts module does not exist so google tts will not work. you can install the python module if you want to use google tts.")



allowedVoices = ['en-us', 'af', 'bs', 'da', 'de', 'el', 'eo', 'es', 'es-la', 'fi', 'fr', 'hr', 'hu', 'it', 'kn', 'ku', 'lv', 'nl', 'pl', 'pt', 'pt-pt', 'ro', 'sk', 'sr', 'sv', 'sw', 'ta', 'tr', 'zh', 'ru']
tempDir = tempfile.gettempdir()
messagesToTTS = []
numActiveEspeak = 0
maximumTTSTime = 5

currentWebsocket = {'chat': None, 'control': None}
lastPongTime = {'chat': datetime.datetime.now(), 'control': datetime.datetime.now()}
websocketOK = {}


print("temporary directory:", tempDir)


parser = argparse.ArgumentParser(description='start robot control program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--forward', default='[-1,1,-1,1]')
parser.add_argument('--left', default='[1,1,1,1]')
parser.add_argument('--no-secure-cert', dest='secure_cert', action='store_false')
parser.add_argument('--voice-number', type=int, default=1)
parser.add_argument('--male', dest='male', action='store_true')
parser.add_argument('--tts-synth', default="espeak", help='options: espeak, festival, google, local_service')
parser.add_argument('--play-nontts-softly', dest='play_nontts_softly', action='store_true')
parser.add_argument('--enable-ping-pong', dest='enable_ping_pong', action='store_true')
parser.set_defaults(enable_ping_pong=False)
parser.add_argument('--tts-volume', type=int, default=80)
parser.add_argument('--audio-output-hardware-name', default=None)
parser.add_argument('--audio-output-hardware-number', type=int, default=None)
parser.add_argument('--tts-pitch', type=int, default=50)
parser.add_argument('--type', default="rsbot")
parser.add_argument('--no-tls-chat', dest='tls_chat', action='store_false')
parser.set_defaults(tls_chat=True)
parser.add_argument('--stream-key', default="123")
parser.add_argument('--straight-speed', type=int, default=255)
parser.add_argument('--turn-speed', type=int, default=255)
parser.add_argument('--turn-delay', type=float, default=0.1)
parser.add_argument('--api-url', default="https://api.robotstreamer.com")
parser.add_argument('--disable-volume-set', dest='disable_volume_set', action='store_true')
parser.set_defaults(disable_volume_set=False)
parser.add_argument('--disable-chat', dest='disable_chat', action='store_true')
parser.set_defaults(disable_chat=False)
parser.add_argument('--kill-on-failed-connection', dest='kill_on_failed_connection', action='store_true')
parser.set_defaults(kill_on_failed_connection=False)
parser.add_argument('--free-tts-queue-size', type=int, default=2)
parser.add_argument('--ffmpeg-path', default='/usr/bin/ffmpeg')


commandArgs = parser.parse_args()

print(commandArgs)


apiHost = commandArgs.api_url

if commandArgs.type == "rsbot":
            print("initializing rsbot")
            import rsbot_interface as interface
            interface.init(commandArgs,
                           json.loads(commandArgs.forward),
                           json.loads(commandArgs.left),
                           commandArgs.enable_ping_pong)

elif commandArgs.type == "windows_interface":
            import windows_interface as interface

elif commandArgs.type == "mac":
            import mac_interface as interface
            
elif commandArgs.type == "gopigo3":
            import gopigo3_interface as interface

elif commandArgs.type == "http_example":
            import http_example_interface as interface

elif commandArgs.type == "gopigo":
            import gopigo_interface as interface

elif commandArgs.type == "gopigomessedup":
            import gopigomessedup_interface as interface            

elif commandArgs.type == "roomba":
            import roomba_interface as interface
            interface.init()

elif commandArgs.type == "roomba_kristie":
            import roomba_kristie_interface as interface
            interface.init()
            
elif commandArgs.type == "open_roomba":
            import open_roomba_interface as interface
            interface.init(commandArgs)

elif commandArgs.type == "humanoid":
            import humanoid_interface as interface
            interface.init()

elif commandArgs.type == "v4l2":
            import v4l2_interface as interface
            
elif commandArgs.type == "l298n":
            import l298n_interface as interface
            interface.init()

elif commandArgs.type == "l298niq":
            import l298niq_interface as interface
            interface.init()

elif commandArgs.type == "tank":
            import tank_interface as interface
            interface.init()

elif commandArgs.type == "sbcshop":
            import sbcshop_interface as interface
            interface.init()
            
elif commandArgs.type == "parallaxy":
            import parallaxy_interface as interface
            interface.init()

elif commandArgs.type == "blank":
            import blank_interface as interface

elif commandArgs.type == "serial":
            import serial_interface as interface

elif commandArgs.type == "bot":
            import bot_interface as interface
            interface.init(commandArgs)

else:
    print("loading custom interface", commandArgs.type)
    interface = importlib.import_module(commandArgs.type)
    interface.init(commandArgs) # your interface module should have an init fuction that takes one parameter



# set volume level

# tested for 3.5mm audio jack
#os.system("amixer set PCM -- 100%d%%" % commandArgs.tts_volume)
#if commandArgs.tts_volume > 50:
    #os.system("amixer set PCM -- -100")


def setVolume(percent):
            print("setting volume to", percent, "%")
            for cardNumber in range(0, 5):
                        for numid in range(0,5):
                                    if cardNumber == 1 and numid == 3:
                                                # this is audio input level so don't set it
                                                continue
                                    print("---------------------")
                                    print("setting card number:", cardNumber, "numid:", numid)
                                    os.system("amixer -c %d cset numid=%d %d%%" % (cardNumber, numid, percent))
                                    print("---------------------")
                                    #time.sleep(5)
            

# volume=1 is normal
def espeak(hardwareNumber, message, voice, volume):

            global numActiveEspeak
            
            numActiveEspeak += 1
            print("number of espeaks active", numActiveEspeak)

            try:
                        # tested for USB audio device
                        #os.system("amixer -c 2 cset numid=%d %d%%" %
                        #          (hardwareNumber, commandArgs.tts_volume))
            
                        tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
                        wavFile = os.path.join(tempDir, str(uuid.uuid4()) + ".wav")
                        croppedWavFile = os.path.join(tempDir, str(uuid.uuid4()) + ".wav")
                        f = open(tempFilePath, "w")
                        f.write(message)
                        f.close()
            
                        print('plughw:%d,0' % hardwareNumber)
                        print("commandArgs.male:", commandArgs.male)
                        if commandArgs.male:
                                    print("male")
                                    cmd = 'cat ' + tempFilePath + ' | espeak -p %d -v%s --stdout > %s' % (commandArgs.tts_pitch, voice, wavFile)
                                    print("--------------", cmd)
                                    os.system(cmd)
                        else:
                                    print("female")
                                    cmd = 'cat ' + tempFilePath + ' | espeak -p %d -v%s+f%d -s170 --stdout > %s' % (commandArgs.tts_pitch, voice, commandArgs.voice_number, wavFile)
                                    print("--------------", cmd)
                                    os.system(cmd)

                        if volume == 1:
                                    filterString = ""
                        else:
                                    filterString = "-filter:audio volume=%f" % volume

                        cropCommand = "%s -i %s -ss 0 -to %d %s %s" % (commandArgs.ffmpeg_path, wavFile, maximumTTSTime, filterString, croppedWavFile)
                        print(cropCommand)
                        cropResult = os.system(cropCommand)
                        print("crop result code", cropResult)
                        if cropResult == 0:
                                    print("play cropped")
                                    os.system('aplay -D plughw:%d,0 %s' % (hardwareNumber, croppedWavFile))
                                    os.remove(croppedWavFile)
                        else:
                                    print("play full file")
                                    os.system('aplay -D plughw:%d,0 %s' % (hardwareNumber, wavFile))                             

            
                        os.remove(tempFilePath)
                        os.remove(wavFile)



            except Exception as e:
                        print("something went wrong with espeak:", e)

            numActiveEspeak -= 1
            print("number of espeaks active", numActiveEspeak)


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
                



def say(message, messageVolume, voice='en-us'):

    audioOutputNumber = commandArgs.audio_output_hardware_number
            
    if commandArgs.audio_output_hardware_name is not None:
        audioOutputNumber = audio_util.getAudioPlayingDeviceByName(commandArgs.audio_output_hardware_name)


    os.system("killall espeak")
    
    if voice not in allowedVoices:
        print("invalid voice")
        return
    
    tempFilePath = os.path.join(tempDir, "text_" + str(uuid.uuid4()))
    f = open(tempFilePath, "w")
    f.write(message)
    f.close()


    #os.system('"C:\Program Files\Jampal\ptts.vbs" -u ' + tempFilePath) Whaa?

    if commandArgs.tts_synth == "google":
        # google text to speach api
        if audioOutputNumber is None: # if none specified try many
            for hardwareNumber in (0, 2, 3, 1, 4):
                google_tts.speak(message, hardwareNumber)
        else:
            google_tts.speak(message, audioOutputNumber)
        return

    elif commandArgs.tts_synth == "local_service":
        try:
            audio_util.postToLocalSpeechService(message, audioOutputNumber)
        except Exception as e:
            print(f"An exception occurred: {e}")
        
    elif commandArgs.tts_synth == "festival":
        # festival tts
        os.system('festival --tts < ' + tempFilePath)

    elif commandArgs.tts_synth == "espeak":
        # espeak tts
        #todo: these could be defined in the interface modules perhaps

        if commandArgs.type == "mac":
                _thread.start_new_thread(espeakMac, (message, voice))

        else:
            if audioOutputNumber is None: # if none specified try many
                        for hardwareNumber in (0, 2, 3, 1, 4):
                                    print("starting espeak thread")
                                    #_thread.start_new_thread(espeak, (hardwareNumber, message, voice, messageVolume))
                                    espeak(hardwareNumber, message, voice, messageVolume)
            else:
                                    #_thread.start_new_thread(espeak, (audioOutputNumber, message, voice, messageVolume))
                                    print("espeak on a specific audio output")
                                    espeak(audioOutputNumber, message, voice, messageVolume)
    else:
        raise Exception("invalid option for --tts-synth")

    os.remove(tempFilePath)



def getControlHost():

        url = apiHost+'/v1/get_service/rscontrol'
        response = robot_util.getNoRetry(url, secure=commandArgs.secure_cert)
        response = json.loads(response)
        print("response:", response)

        if response is not None:
            response['protocol'] = 'wss'
            print("get_service response:", response)
        
        if response is None:
            
            url = apiHost+'/v1/get_endpoint/rscontrol_robot/'+commandArgs.robot_id 
            response = robot_util.getNoRetry(url, secure=commandArgs.secure_cert)
            response = json.loads(response)

            if response is not None:
                response['protocol'] = 'ws'
                print("get_endpoint response:", response)

        return response
            
def getChatHost(useTLS):

        url = apiHost+'/v1/get_service/rschat'
        response = robot_util.getNoRetry(url, secure=commandArgs.secure_cert)
        response = json.loads(response)

        if response is not None:
            print("get_service response:", response)
        
        if response is None:
            
            if useTLS:
                url = apiHost+'/v1/get_random_endpoint/rschatssl/100'
            else:
                url = apiHost+'/v1/get_random_endpoint/rschat/100'

            response = robot_util.getNoRetry(url, secure=commandArgs.secure_cert)
            response = json.loads(response)
            print("get_endpoint response:", response)

        return response


async def handleWesocketTester(key):

        while True:
            time.sleep(5)
            if currentWebsocket[key] is not None:
                        print(key.upper()+": sending rs ping message")
                        try:
                            await currentWebsocket[key].send('{"command":"RS_PING"}')
                        except:
                            print(key.upper()+": control ping error") 
            else:
                        print(key.upper()+": control websocket is not initialized")


            elapsed = datetime.datetime.now() - lastPongTime[key]
            print(key.upper()+": elapsed time since last acklowledgement (%s):" % key,
                  elapsed.total_seconds())
            if (elapsed.total_seconds() > 60):
                        print(key.upper()+": test failed, signaling restart")
                        websocketOK[key] = False

                                    

async def handleControlMessages():

    h = getControlHost()

    url = '%s://%s:%s/echo' % (h['protocol'], h['host'], h['port'])
    print("CONTROL url:", url)

    async with websockets.connect(url) as websocket:

        print("CONTROL: control websocket object:", websocket)

        if h['protocol'] == 'wss': 
            # validation handshake new
            await websocket.send(json.dumps({"type":"robot_connect",
                                             "robot_id":commandArgs.robot_id,
                                             "stream_key":commandArgs.stream_key}))
        else:
            # validation handshake old
            await websocket.send(json.dumps({"command":commandArgs.stream_key}))


        currentWebsocket['control'] = websocket
        
        while True:

            print("CONTROL: awaiting control message")
            
            message = await websocket.recv()
            #print("< {}".format(message))
            j = json.loads(message)
            print("CONTROL message: ",j)

            if j.get('command') == "RS_PONG":
                        lastPongTime['control'] = datetime.datetime.now()

            if j.get('type') == "RS_PING":
                        #ws keepalive new
                        lastPongTime['control'] = datetime.datetime.now()

            elif j.get('command') and j.get('key_position'): # apparently use of _thread for this on new os (2021) causes seg fault
                _thread.start_new_thread(interface.handleCommand, (j["command"],
                                                                   j["key_position"],
                                                                   j.get('command_price', 0)))


            
async def handleChatMessages():

    h = getChatHost(commandArgs.tls_chat)

    if h == False:
        raise Exception("failed to get valid chat host")

    if commandArgs.tls_chat: h['protocol'] = 'wss'
    else: h['protocol'] = 'ws'

    url = '%s://%s:%s/echo' % (h['protocol'], h['host'], h['port'])
    print("CHAT url:", url)

    async with websockets.connect(url) as websocket:

        print("CHAT connected to chat service at: ", url)
        print("CHAT chat websocket object: ", websocket)

        # removed comment: you do need this as an connection initializer, but you should make the server not need it
        # chat server requires atleast a robot_id for when non global chat is enforced but otherwise no initialiser required
        # treat stream_key as token when type robot_connect for future use
        await websocket.send(json.dumps({"type":"robot_connect",
                                         "token":str(commandArgs.stream_key),
                                         "robot_id":str(commandArgs.robot_id) }))     

        currentWebsocket['chat'] = websocket
        
        while True:

            print("CHAT: awaiting chat message")
            
            message = await websocket.recv()
            #print("< {}".format(message))
            j = json.loads(message)
            print("CHAT message:", j)


            if j.get('command') == "RS_PONG":
                lastPongTime['chat'] = datetime.datetime.now()

            elif j.get('type') == "RS_PING":
                print("CHAT: RS_PING keepalive")

            elif ('message' in j) and (j['robot_id'] == commandArgs.robot_id):
                            if ('tts' in j) and j['tts'] == True:
                                        print("CHAT: tts option is on")
                                        # paid messages can queue but unpaid cannot
                                        if len(messagesToTTS) < commandArgs.free_tts_queue_size or (('tts_price' in j) and (j['tts_price'] >= 0.01)):
                                                    messagesToTTS.append((j['message'], 1))
                            else:
                                        print("CHAT: tts option is off")
                                        if commandArgs.play_nontts_softly:
                                                    if len(j['message']) > 0:
                                                                if len(messagesToTTS) == 0:
                                                                            messagesToTTS.append((j['message'][1:], 0.15))
                            #if audio.espeakBytes(j['message']) < 400000:
                            #            print("length", audio.espeakBytes(j['message']))
                            #            _thread.start_new_thread(say, (j['message'],))
                            #else:
                            #            print("message too long")
            else:
                print("CHAT: error, message not valid:", j)



def startWebsocketTester(key):
    print(key.upper()+": tester, waiting a few seconds")
    time.sleep(6) #todo: only wait as needed (wait for interent)

    if True:
                print(key.upper()+": starting tester loop")
                time.sleep(1)
                try:
                            asyncio.new_event_loop().run_until_complete(handleWesocketTester(key))
                except:
                            print(key.upper()+" :error")
                            traceback.print_exc()
                print(key.upper()+": socket tester event handler died so killing process")
                time.sleep(2)



def startControl():
    print("CONTROL: waiting a few seconds")
    time.sleep(6) #todo: only wait as needed (wait for internet) note:has a retry now

    while True:
                print("CONTROL: starting control loop")
                try:
                            asyncio.new_event_loop().run_until_complete(handleControlMessages())
                except:
                            print("CONTROL: error")
                            traceback.print_exc()
                print("CONTROL: control event handler died")
                # sleep to stop hammering endpoint requests
                time.sleep(2)
                interface.movementSystemActive = False
    


def startChat():
        time.sleep(10) #todo: only wait as needed (wait for interenet)
        print("restarting loop")
        time.sleep(0.25)

        while True:
                    print("CHAT: starting chat loop")
                    
                    try:
                                asyncio.new_event_loop().run_until_complete(handleChatMessages())
                    except:
                                print("CHAT: error")
                                traceback.print_exc()
                    print("CHAT: event handler died")
                    # sleep to stop hammering endpoint requests
                    time.sleep(2)

#async def hello(uri):
#       async with websockets.connect(uri) as websocket:
#                await websocket.send(json.dumps({"message":"message"}))
#                while True:
#                        print("recv")
#                        x = await websocket.recv()
#                        print(x)



def runPeriodicTasks():

            for key in websocketOK:
                        if not websocketOK[key] and commandArgs.kill_on_failed_connection:
                                    print("exiting because the " + key + " connection has failed")
                                    exit(1)

            
            if robot_util.getSoundQueueSize() < 1:
                if len(messagesToTTS) > 0 and numActiveEspeak == 0 and robot_util.getNumActiveSounds() == 0:
                            message, messageVolume = messagesToTTS.pop(0)
                            #_thread.start_new_thread(say, (message, messageVolume))
                            say(message, messageVolume)
            else:
                if numActiveEspeak == 0 and robot_util.getNumActiveSounds() == 0:
                    _thread.start_new_thread(robot_util.aplayFile, (robot_util.popSoundQueue(),))
                        

            
def main():                

                       
            print(commandArgs)
            
            _thread.start_new_thread(startControl, ())
            websocketOK['control'] = True # enable tester

            if not commandArgs.disable_chat:

                _thread.start_new_thread(startChat, ()) 
                websocketOK['chat'] = True # enable tester

            for key in websocketOK:
                # run tester
                _thread.start_new_thread(startWebsocketTester, (key,))


            if not commandArgs.disable_volume_set:
                setVolume(commandArgs.tts_volume)

            while True:
                time.sleep(0.20)
                runPeriodicTasks()


                
if __name__ == '__main__':
    main()


