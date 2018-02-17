
import asyncio
import websockets
import time
import argparse
import rsbot_python36 as rsbot
import json
import robot_util_python36 as robot_util



apiHost = "robotstreamer.com:6001"


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
            

async def hello():

    port = getControlHostPort()['port']
    print("connecting to port:", port)
    url = 'ws://54.219.37.103:%s/echo' % port

    async with websockets.connect(url) as websocket:

        print("connected to control service at", url)
        print("websocket object:", websocket)
        
        count = 0
        
        while True:

            print("awaiting message")
            
            message = await websocket.recv()
            print("< {}".format(message))
            j = json.loads(message)
            print(j)
            rsbot.move(j["command"])
            count = count + 1

asyncio.get_event_loop().run_until_complete(hello())




