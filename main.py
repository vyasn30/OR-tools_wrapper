from vrpLevers import Coors, Network, vrpWrap, DataModel, Node, Vehicle

if __name__ == '__main__':
  coors = []
  ctr = 0
  isDepot = False
  demands = []
  numberOfVehicles = None
  fleet  = []
  myNodes = []


  while True:    #loop for nodes
    wantToEnter=True if input("Want to enter a node? -> ").lower()=="y" else False
    print(wantToEnter)
    if wantToEnter==True:
      
      address = input("Enter address of the node -> ")
      demand = input("Enter the demand of the node -> ")
      try:      
        coor = Coors(geoString = address)
      except:
        print("Please reEnter")
        continue
      myNodes.append(Node(coor, demand))
      print(coor.latitude, coor.longitude)
       
    else:
      break

  numberOfVehicles = int(input("Enter the number of Vehicles -> "))
  
  for i in range(0, numberOfVehicles):
    capacity = int(input("Enter the capacity of the vehicle -> "))
    fleet.append(Vehicle(capacity))


  depotIndex = int(input("Enter Depot index -> "))
  network =Network(depotNode = depotIndex, numVehicles=numberOfVehicles, nodes = myNodes, vehicles = fleet)

  vrp = vrpWrap(DataModel(network).getData())
  solution = vrp.solve()
  print(vrp.print_solution())
