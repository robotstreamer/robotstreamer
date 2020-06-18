
import requests 
from time import sleep
  
for i in range(10):

  print(i)

  URL = "http://192.168.178.28/"
  
  #URL = "https://postman-echo.com/"
  
  PARAMS = {'value':50}
  print(URL, PARAMS)
  r = requests.get(url = URL, params = PARAMS) 
  #data = r.json() 
  print(r.content)
  
  sleep(1)

  
  PARAMS = {'value':120} 
  print(URL, PARAMS)
  r = requests.get(url = URL, params = PARAMS) 
  #data = r.json() 
  print(r.content)

  sleep(1)


