import requests
import re
from time import sleep

URL = "http://127-0-0-1.lovense.club:20010/Vibrate"

def init():
  print("init")
                

def getVibrateParams(command):
    expression = re.compile('vibrate([0-9]+)duration([0-9]+)')
    matches = expression.match(command)
    if matches is None:
        print("match failed. command should be like vibrate<power>duration<time> for example vibrate10duration1")
        return None, None
    power = matches.group(1)
    duration = matches.group(2)
    return int(power), int(duration)


def handleCommand(command, keyPosition):

    print("***********************************", command)
    power, duration = getVibrateParams(command)
    if power is not None:
      print('\a')
      print("command is " + str(command))
      PARAMS = {'v':power}
      print(URL, PARAMS)
      r = requests.get(url = URL, params = PARAMS) 
      print(r)
      print(r.content)
      sleep(duration)
      PARAMS = {'v':0}
      print(URL, PARAMS)
      r = requests.get(url = URL, params = PARAMS) 
      print(r)
      print(r.content)

                



