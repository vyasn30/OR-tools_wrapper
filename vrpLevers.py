from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from sklearn.neighbors import DistanceMetric

def calculateDistance(coor1, coor2):
  return math.sqrt((coor1.x-coor2.x)**2 + (coor1.y-coor2.y)**2)

class Coors:
  def __init__(self, latitude, longitude):
    self.latitude = latitude
    self.longitude = longitude

class TimingWindow:
  def __init__(self, startTime, endTime):
    self.startTime =  startTime
    self.endTime = endTime
    
  

class Node:
  def __init__(self, coors, timingWindow=None):
    self.timingWindow = timingWindow
    self.coors = coors
    self.id = id(self)


class Network:
  def __init__(self, nodes, depotNode, numVehicles):
    self.nodes = nodes
    self.depot = depotNode
    self.numVehicles = numVehicles
    print(self.numVehicles)
  

class DataModel:
  def __init__(self, network):
    self.data = {}
    self.network = network
    self.data["num_vehicles"] = self.network.numVehicles
    self.data["depot"] = self.network.depot
    


  def calculateDistanceMatrix(self):
    nodeCoorList =[[np.radians(node.coors.latitude), np.radians(node.coors.longitude)] for node in network.nodes]
    

    metric = DistanceMetric.get_metric("haversine")
    self.data["distance_matrix"] =  metric.pairwise(nodeCoorList)*6373

      
     


  def getData(self):
    self.calculateDistanceMatrix()
    return self.data
  
  


class vrpWrap:
  def __init__(self, data):
    self.data = data
    self.manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    self.routingManager = pywrapcp.RoutingModel(self.manager)
    self.transit_callback_index = None 


  def addDistanceDimension(self):
    self.routingManager.AddDimension(
        self.transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        "Distance"
      )
    
    distance_dimension = self.routingManager.GetDimensionOrDie("Distance")
    distance_dimension.SetGlobalSpanCostCoefficient(100)



  def distanceCallback(fromIndex, toIndex):
    fromNode = self.manager.IndextoNode(fromIndex)
    toNode = self.manager.IndextoNode(toIndex)

    return self.data['distance_matrix'][fromNode][toNode]

  def solve(self):
    self.transit_callback_index = self.routingManager.RegisterTransitCallback(self.distanceCallback)

    self.routingManager.SetArcCostEvaluatorOfAllVehicles(self.transit_callback_index)
    
    self.addDistanceDimension()
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = self.routingManager.SolveWithParameters(search_parameters)

    return solution




    




if __name__ == '__main__':
  nodes = []

  coor1 = Coors(12.9716,77.5946)
  coor2 = Coors(19.076,72.877)
  coor3 = Coors(28.7041,77.1025)
  coor4 = Coors(13.0827, 80.2707)

  node1 = Node(coor1)
  node2 = Node(coor2)
  node3 = Node(coor3)

  nodes.append(node1)
  nodes.append(node2)
  nodes.append(node3)

  for val in nodes:
    print(val.id)

 
  network =  Network(nodes, 0, 1)
  print(DataModel(network).getData())



  vrp = vrpWrap(DataModel(network).getData())
  print(vrp.solve())
