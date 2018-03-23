
import os
import asyncio
import websockets
import time
import argparse
import json
import _thread
import traceback
import subprocess
import urllib
import urllib.request


config = json.load(open('config.json'))

userID = "26"

chatEndpoint = {'host': '184.72.15.121', 'port': 8765}
parser = argparse.ArgumentParser(description='robotstreamer chat bot')
commandArgs = parser.parse_args()




def jsonResponsePOST(url, jsonObject):

    print("json object to POST", jsonObject)

    params = json.dumps(jsonObject).encode('utf8')
    req = urllib.request.Request(url, data=params,
                             headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    jsonResponse = json.loads(response.read())
    
    print("response:", jsonResponse)
   
    return jsonResponse
    

    
        
async def handleStatusMessages():

    global mainWebsocket

    print("running handle status messages")

    url = 'ws://%s:%s' % (chatEndpoint['host'], chatEndpoint['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        mainWebsocket = websocket
    
        print("connected to service at", url)
        print("chat websocket object:", websocket)

        print("starting websocket.send")
        #await websocket.send(json.dumps({"type":"connect",
        #                                 "robot_id":1,
        #                                 "local_address":"1"}))

        while True:

            print("awaiting message, this is optional (Ctrl-Break in Windows to Break)")
            message = await websocket.recv()
            print("received message:", message)
            



async def handleUpdateMessages():                
    
    global mainWebsocket
    count = 0
    print("start update")
    while True:
            time.sleep(2)
            print("sending")
            m = "!play https://youtubewhatever  to play a song"
            if count % 2 == 0:
                m = m + " "
            print("message to send:", m)
            await mainWebsocket.send(json.dumps({"message": m,
                                                                     "token": config['jwt_user_token']}))
            count += 1
            time.sleep(160*5)
                
            
            
            
def startStatus():
        print("starting status")
        try:
                asyncio.new_event_loop().run_until_complete(handleStatusMessages())
        except:
                print("error")
                traceback.print_exc()

                
def startUpdateMessages():
        print("starting status")
        try:
                asyncio.new_event_loop().run_until_complete(handleUpdateMessages())
        except:
                print("error")
                traceback.print_exc()
                



def main():                

    print(commandArgs)
    print("starting chat bot")
    _thread.start_new_thread(startStatus, ())
    _thread.start_new_thread(startUpdateMessages, ())
    
    # wait forever
    while True:
        time.sleep(5)

                
if __name__ == '__main__':
    main()


