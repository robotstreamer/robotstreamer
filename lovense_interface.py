import requests 
from time import sleep

URL = "http://127-0-0-1.lovense.club:20010/Vibrate"

def init():
  print("init")
                
    
def handleCommand(command, keyPosition):

                print("***********************************", command)
                if command == 'F':
                  print("command is F")
                  PARAMS = {'v':50}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)
                  sleep(3)
                  PARAMS = {'v':0}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)


                if command == 'B':
                  print("command is B")
                  PARAMS = {'v':100}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)
                  sleep(3)      
                  PARAMS = {'v':0}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)
                



