
import os
import asyncio
import websockets
import time
import argparse
import json
import _thread
import traceback
import subprocess



statusEndpoint = {'host': '184.72.15.121', 'port': 6020}



parser = argparse.ArgumentParser(description='start reverse ssh program')
parser.add_argument('robot_id', help='Robot ID')
parser.add_argument('--reverse-ssh-host', default='ubuntu@52.52.223.119')
parser.add_argument('--reverse-ssh-key-file', default='/home/pi/rsjumpbox0.pem')


commandArgs = parser.parse_args()

robotID = commandArgs.robot_id

print("robot id:", robotID)



def startReverseSSH():
    print("starting reverse ssh process")
    returnCode = subprocess.call(["/usr/bin/ssh",
                                  "-X",
                                  "-i", commandArgs.reverse_ssh_key_file,
                                  "-N",
                                  "-R", "2222:localhost:22",
                                  commandArgs.reverse_ssh_host])
    print("return code", returnCode)


def stopReverseSSH():
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

        #todo: you do need this as an connection initializer, but you should make the server not need it
        await websocket.send(json.dumps({"type":"connect",
                                         "robot_id":robotID}))     

        while True:

            print("awaiting message")
            
            message = await websocket.recv()
            print("received message:", message)
            j = json.loads(message)
            print("json message:", j)

            if 'type' in j:
                t = j['type']
                if t == "start_reverse_ssh":
                        _thread.start_new_thread(startReverseSSH, ())
                elif t == "stop_reverse_ssh":
                        _thread.start_new_thread(stopReverseSSH, ())
                        
            else:
                    print("invalid message:", j)
            



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


