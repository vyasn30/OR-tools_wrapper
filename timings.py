import time
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim

key = "hw5ODt9aNcsJZfFmk8XVcRrU1VQx7zWa" 

def geoStringsToCoors(geoStringList):
  coorList = []
  for geoString in geoStringList:
    locator = Nominatim(user_agent = "myGeocoder")
    location = locator.geocode(geoString)
    coor = []
    coor.append(location.latitude)
    coor.append(location.longitude)
    coorList.append(coor)

  return coorList
    


def getTimeMatrix(geoStringList):
  geoList = geoStringsToCoors(geoStringList)
  print(geoList)
  timeMatrix = [[0 for i in range(len(geoList))] for j in range(len(geoList))]
  print(timeMatrix)

  for i in range(len(geoList)):
    for j in range(len(geoList)):
      if i==j:
        continue
      
      timeMatrix[i][j] = getTime(geoList[i], geoList[j])

  print(timeMatrix)
      



def getTime(coor1, coor2):
  r = requests.get(
    "https://api.tomtom.com/routing/1/calculateRoute/" +str    (coor1[0])+ "," + str(coor1[1]) + ":" + str(coor2[0])    + "," + str(coor2[1]) + "/xml?avoid=unpavedRoads&key=" + key
  )

  print(r)
  
  c = r.content
  soup = BeautifulSoup(c, "html.parser")
  soup.prettify()
  
  travelTime = int(soup.find('traveltimeinseconds').get_text())
  return travelTime



if __name__=="__main__":
  geoStringList = ["Ambawadi Circle, Ahmedabad", "Club 07, Bopal", "Naroda Patiya", "The Fern Hotel, Sola", "Trimandir, Adalaj"]
  
  getTimeMatrix(geoStringList)
 
  


