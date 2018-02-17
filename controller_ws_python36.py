
import asyncio
import websockets
import time
import argparse
import rsbot_python36 as rsbot
import json




parser = argparse.ArgumentParser(description='start robot control program')


parser.add_argument('--forward', default='[-1,1,-1,1]')
parser.add_argument('--left', default='[1,1,1,1]')


commandArgs = parser.parse_args()


rsbot.init(json.loads(commandArgs.forward),
           json.loads(commandArgs.left))






async def hello():

    url = 'ws://54.219.37.103:9310/echo'

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




