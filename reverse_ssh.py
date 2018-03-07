
import os
import asyncio
import websockets
import time
import argparse
import json
import robot_util_python36 as robot_util
import _thread
import traceback
import tempfile
import uuid



statusEndpoint = {'host': '184.72.15.121', 'port': 6020}



parser = argparse.ArgumentParser(description='start reverse ssh program')
parser.add_argument('robot_id', help='Robot ID')


commandArgs = parser.parse_args()



            
async def handleStatusMessages():

    print("running handle status messages")

    url = 'ws://%s:%s' % (statusEndpoint['host'], statusEndpoint['port'])
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


            



def startStatus():
        time.sleep(2) #todo: only wait as needed (wait for interenet)
        print("restarting loop")


        
        try:
                asyncio.new_event_loop().run_until_complete(handleStatusMessages())
        except:
                print("error")
                traceback.print_exc()


                

        
def main():                
                       
            print(commandArgs)
            print("starting")
            startStatus()


                
if __name__ == '__main__':
    main()


