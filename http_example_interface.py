import requests 
from time import sleep

URL = "http://192.168.178.28/"


def init():
  print("init")
                
    
def handleCommand(command, keyPosition):

                print("***********************************", command)
                if command == 'F':
                  print("command is F")
                  PARAMS = {'value':50}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)


                if command == 'B':
                  print("command is B")
                  PARAMS = {'value':100}
                  print(URL, PARAMS)
                  r = requests.get(url = URL, params = PARAMS) 
                  print(r)
                  print(r.content)
                        
                



                

            

# routing

#{"F": forward, "B": back, "L": left, "R": right}
