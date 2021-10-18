import requests 
from time import sleep

URL = "http://127-0-0-1.lovense.club:20010/Vibrate"

def init():
  print("init")
                

def getSpeed(command):
  # assume the command is like vibrate50 or vibrate100
  return int(command[7:])

def handleCommand(command, keyPosition, price=0):

                print("***********************************", command)
                if command[0:7] == 'vibrate':
                  print('\a')
                  print("command is " + str(command))
                  PARAMS = {'v':getSpeed(command)}
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

                



