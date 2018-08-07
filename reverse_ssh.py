
import os
import sys
import asyncio
import websockets
import time
import argparse
import json
import _thread
import traceback
import subprocess



statusEndpoint = {'host': 'robotstreamer.com', 'port': 6020}



parser = argparse.ArgumentParser(description='start reverse ssh program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--reverse-ssh-host', default='ubuntu@52.52.223.119')
parser.add_argument('--reverse-ssh-key-file', default='/home/pi/rsjumpbox0.pem')


commandArgs = parser.parse_args()

robotID = commandArgs.robot_id

print("robot id:", robotID)



async def startReverseSSH(websocketToStatusService):
    print("starting reverse ssh process")


    await websocketToStatusService.send(json.dumps({"type": "info",
                                                    "result": "starting reverse ssh process on robot"}))

    
    try:
            result = subprocess.check_output(["/usr/bin/ssh",
                                  "-X",
                                  "-i", commandArgs.reverse_ssh_key_file,
                                  "-N",
                                  "-R", "2222:localhost:22",
                                  "-o", "StrictHostKeyChecking=no",
                                                  commandArgs.reverse_ssh_host], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
            result = str(e.returncode) + " " + str(e.output)
    except:
            result = sys.exc_info()[0]
            traceback.print_exc()

            
    print("sending start reverse ssh info message to", websocketToStatusService)
    await websocketToStatusService.send(json.dumps({"type": "info",
                                                    "result": "reverse ssh process finished running: " + str(result)}))

    print("reverse ssh result", result)


async def stopReverseSSH(senderWebsocket):
    print("handling stop reverse ssh process")
    resultCode = subprocess.call(["killall", "ssh"])
    print("result code of killall ssh:", resultCode)

    
async def handleStatusMessages():

    print("running handle status messages")

    url = 'ws://%s:%s' % (statusEndpoint['host'], statusEndpoint['port'])
    print("chat url:", url)

    async with websockets.connect(url) as websocket:

        print("connected to control service at", url)
        print("chat websocket object:", websocket)

        print("starting websocket.send")
        await websocket.send(json.dumps({"type":"connect",
                                         "robot_id":robotID,
                                         "local_address":subprocess.check_output(["hostname", "-I"]).decode("utf-8").strip()}))

        while True:

            print("awaiting message")
            
            message = await websocket.recv()
            print("received message:", message)
            j = json.loads(message)
            print("json message:", j)

            if 'type' in j:
                t = j['type']
                if t == "start_reverse_ssh":
                        f = lambda: asyncio.new_event_loop().run_until_complete(startReverseSSH(websocket))
                        _thread.start_new_thread(f, ())
                        print("finished sending start reverse ssh. it should be running now")
                elif t == "stop_reverse_ssh":
                        await stopReverseSSH(websocket)
                        print("finished sending stop reverse ssh")
            else:
                    print("invalid message:", j)
            




def startStatus():

        while True:
                time.sleep(2) #todo: only wait as needed (wait for interenet)
                print("starting asyncio new event loop")

        
                try:
                        asyncio.new_event_loop().run_until_complete(handleStatusMessages())
                except:
                        print("error: asyncio.new_event_loop has crashed")
                        traceback.print_exc()


                

        
def main():                
                       
            print(commandArgs)
            print("starting")
            startStatus()


                
if __name__ == '__main__':
    main()


