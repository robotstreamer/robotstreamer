
import requests 
  
for i in range(10):

  print(i)

  URL = "http://192.168.178.28/?value=50"
  PARAMS = {'value':50}
  print(URL, PARAMS)
  r = requests.get(url = URL, params = PARAMS) 
  data = r.json() 
  print(data)
  
  sleep(1)

  URL = "http://192.168.178.28/?value=100"
  PARAMS = {'value':120} 
  print(URL, PARAMS)
  r = requests.get(url = URL, params = PARAMS) 
  data = r.json() 
  print(data)

  sleep(1)


