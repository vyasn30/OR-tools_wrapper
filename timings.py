import time
import requests
from bs4 import BeautifulSoup

key = "hw5ODt9aNcsJZfFmk8XVcRrU1VQx7zWa" 





def getTime(coor1, coor2):
  r = requests.get(
    "https://api.tomtom.com/routing/1/calculateRoute/" +str    (coor1[0])+ "," + str(coor1[1]) + ":" + str(coor2[0])    + "," + str(coor2[1]) + "/xml?avoid=unpavedRoads&key=" + key
  )

  print(r)
  
  c = r.content
  soup = BeautifulSoup(c)
  soup.prettify()
  
  travelTime = int(soup.find('traveltimeinseconds').get_text())
  return travelTime



if __name__=="__main__":
  coor1 = (23.020989, 72.553821)
  coor2 = (23.177812, 72.571873)
  print(getTime(coor1, coor2))
