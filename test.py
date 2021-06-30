from geopy.geocoders import Nominatim


while True:
  locator = Nominatim(user_agent="myGeocoder")
  location = locator.geocode(input())
  print(location.latitude, location.longitude)

