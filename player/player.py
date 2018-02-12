import thread
import time
import json
import subprocess
import validators




from socketIO_client import SocketIO, LoggingNamespace




def waitForChatServer():
    while True:
        chatSocket.wait(seconds=1)        


def startListenForChatServer():
   thread.start_new_thread(waitForChatServer, ())

  
chatSocket = SocketIO("54.219.138.36", 6776, LoggingNamespace)


print chatSocket

startListenForChatServer()



def handle_chat_message(args):
    if args[0] == '2':
        return # this should not be needed
    j = json.loads(args)
    print j['message']

    m = j['message']
    print "m:", m
    if m[0:5] == "!play":
        message = m.split(" ")[1]
    
        print m.split(" ")
    
        if message[0:12] == "youtube.com/" or message[0:15] == "www.youtube.com/" or message[0:24] == "https://www.youtube.com/" or message[0:17] == "https://youtu.be/" or message[0:23] == "https://soundcloud.com/":
                if validators.url(message):
                    url = message
                    print "playing", url
                    subprocess.call(["Taskkill", "/IM", "firefox.exe", "/F"])
                    subprocess.Popen(["C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe", url])
                else:
                    print "not valid url in general"
        else:
                print "not valid url for youtube"
                
                
                
    
    
    
    
    
    
    
    
    
        



def onHandleChatMessage(*args):
   thread.start_new_thread(handle_chat_message, args)

   
   
chatSocket.on('message', onHandleChatMessage);


while True:
    time.sleep(1)



