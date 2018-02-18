
import asyncio
import websockets
import time
import argparse
import rsbot_python36 as rsbot
import json
import robot_util_python36 as robot_util
import _thread
import traceback



apiHost = "robotstreamer.com:6001"
controlHost = "robotstreamer.com"
chatHostPort = {"host":"54.219.138.36", "port":8765}



parser = argparse.ArgumentParser(description='start robot control program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--forward', default='[-1,1,-1,1]')
parser.add_argument('--left', default='[1,1,1,1]')
parser.add_argument('--no-secure-cert', dest='secure_cert', action='store_false')




commandArgs = parser.parse_args()


rsbot.init(json.loads(commandArgs.forward),
           json.loads(commandArgs.left))




def getControlHostPort():

        url = 'http://%s/get_control_host_port/%s' % (apiHost, commandArgs.robot_id)
        response = robot_util.getWithRetry(url, secure=commandArgs.secure_cert)
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
            rsbot.move(j["command"])


            
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
            print(j)

            

            
def startControl():
        print ("restarting loop")
        time.sleep(0.25)
        try:
                asyncio.new_event_loop().run_until_complete(handleControlMessages())
        except:
                print("error")
                traceback.print_exc()



def startChat():
        print ("restarting loop")
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
        
                

_thread.start_new_thread(startControl, ())
_thread.start_new_thread(startChat, ())
#_thread.start_new_thread(startTest, ())
#startTest()

while True:
        time.sleep(1)



