from vrpLevers import Coors, Network, vrpWrap, DataModel

if __name__ == '__main__':
  coors = []
  ctr = 0
  isDepot = False
  while True:
    wantToEnter=True if input("Want to enter a node?").lower()=="y" else False
    print(wantToEnter)
    if wantToEnter==True:
      
      latitude, longitude = tuple(map(float, input("Enter coors").split(",")))
      coor = Coors(latitude, longitude)
      coors.append(coor)

    else:
      break

  numberOfVehicles = int(input("Enter the number of Vehicles"))
  print(coors)
  depotIndex = int(input("Enter Depot index"))

  network = Network(depotIndex, numberOfVehicles)
  for coor in coors:
    network.addNode(coor)

  vrp = vrpWrap(DataModel(network).getData())
  solution = vrp.solve()
  print(vrp.print_solution())
