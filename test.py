from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from vrpLevers import Coors, Node, Network, vrpWrap, DataModel




if __name__ == '__main__':
  coors = [Coors(40.748817, -73.985428),Coors(40.743057, -73.972162)
           ,Coors(40.748359, -73.990814),Coors(40.743823, -73.995250)
           ,Coors(40.754181, -73.989855), Coors(40.754181, -73.989340)
           , Coors(40.754599, -73.994061), Coors(40.739551, -73.988505)
           , Coors(40.736550, -73.979024), Coors(40.755834, -73.983573)
           ]

  network = Network(0,1)
  

  for coor in coors:
    network.addNode(coor)
  print(DataModel(network).getData())



