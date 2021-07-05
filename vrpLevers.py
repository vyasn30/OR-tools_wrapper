from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from sklearn.neighbors import DistanceMetric
from geopy.geocoders import Nominatim

class Coors:
  def __init__(self, latitude=None, longitude=None, geoString = None):
    self.latitude = latitude
    self.longitude = longitude
    self.geoString = geoString
    if self.geoString:
      locator = Nominatim(user_agent = "myGeocoder")
      location = locator.geocode(geoString)
      self.latitude = location.latitude
      self.longitude = location.longitude
   
class Vehicle:
  def __init__(self, capacity):
    self.capacity = capacity

   
class TimingWindow:
  def __init__(self, startTime, endTime):
    self.startTime =  startTime
    self.endTime = endTime
    
  

class Node:
  def __init__(self, coors, demand = None):
    self.coors = coors
    self.id = id(self)
    self.demand = demand

class Network:
  def __init__(self, depotNode = 0, numVehicles=1, nodes = None, vehicles = None, pickups_deliveries = None):
    self.nodes = []
    self.depot = depotNode
    self.numVehicles = numVehicles
    self.vehicles = vehicles
    self.pickups_deliveries = pickups_deliveries
  
  def addNodeToNetwork(self, node):
    self.nodes.append(node)


  def addNodeFromCoors(self, coors):
    newNode = Node(coors)
    self.nodes.append(newNode)
  

class DataModel:
  def __init__(self, network):
    self.data = {}
    self.network = network
    self.data["num_vehicles"] = self.network.numVehicles
    self.data["depot"] = self.network.depot
    self.data["names"] = [] 
    self.data["demands"] = []
    self.data["vehicle_capacities"] = []
    self.data["pickups_deliveries"] = []
  


  def calculateDistanceMatrix(self):
    nodeCoorList =[[np.radians(node.coors.latitude), np.radians(node.coors.longitude)] for node in self.network.nodes]
    
    metric = DistanceMetric.get_metric("haversine")
    self.data["distance_matrix"] =  metric.pairwise(nodeCoorList)*6373

  def assignNames(self):
    self.data["names"] = [node.coors.geoString for node in self.network.nodes]
     
  def setDemands(self):
    for node in self.network.nodes:
      self.data["demands"].append(node.demand)

  def setVehicleCapacities(self):
    for vehicle in self.network.vehicles:
      self.data["vehicle_capacities"].append(vehicle.capacity)
  def setPickupsAndDeliveries(self):
    self.data["pickups_deliveries"] = self.network.pickups_deliveries

  def getData(self):
    self.setVehicleCapacities()
    self.setDemands()
    self.assignNames()
    self.calculateDistanceMatrix()
    self.setPickupsAndDeliveries()
    return self.data
  
  


class vrpWrap:
  def __init__(self, data):
    self.data = data
    self.manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    self.routingManager = pywrapcp.RoutingModel(self.manager)
    self.transit_callback_index = None 
    self.solution = None
    self.demand_callback_index = None
    self.distace_dimension = None

  def addDistanceDimension(self):
    self.routingManager.AddDimension(
        self.transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        "Distance"
      )
    self.distance_dimension = self.routingManager.GetDimensionOrDie("Distance")
    self.distance_dimension.SetGlobalSpanCostCoefficient(100)

  def addCapacityDimension(self):
    self.routingManager.AddDimensionWithVehicleCapacity(
      self.demand_callback_index,
      0,  
      self.data["vehicle_capacities"], 
      True,
      "Capacity"
    )
    


  def distanceCallback(self, fromIndex, toIndex):
    fromNode = self.manager.IndexToNode(fromIndex)
    toNode = self.manager.IndexToNode(toIndex)
    return self.data['distance_matrix'][fromNode][toNode]


  def demandCallback(self, fromIndex):
    fromNode = self.manager.IndexToNode(fromIndex)
    return self.data['demands'][fromNode]
  


  def solve(self):
    self.transit_callback_index = self.routingManager.RegisterTransitCallback(self.distanceCallback)
    
    self.routingManager.SetArcCostEvaluatorOfAllVehicles(self.transit_callback_index)

    self.demand_callback_index = self.routingManager.RegisterUnaryTransitCallback(self.demandCallback)
    

    self.addDistanceDimension()
    self.addCapacityDimension()


    if self.data["pickups_deliveries"]:
      for request in self.data["pickups_deliveries"]:
        pickup_index = self.manager.NodeToIndex(request[0])
        delivery_index = self.manager.NodeToIndex(request[1])
        self.routingManager.AddPickupAndDelivery(
          pickup_index, delivery_index
        )
        self.routingManager.solver().Add(
          self.routingManager.VehicleVar(pickup_index) == self.routingManager.VehicleVar(delivery_index)
        )

        self.routingManager.solver().Add(
          self.distance_dimension.CumulVar(pickup_index) <= self.distance_dimension.CumulVar(delivery_index)
        )
    

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.FromSeconds(1)

    self.solution = self.routingManager.SolveWithParameters(search_parameters)

    return self.solution
  

  def print_solution(self):
    """Prints solution on console."""
    print(f'Objective: {self.solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    max_route_distance = 0
    for vehicle_id in range(self.data['num_vehicles']):
        index = self.routingManager.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not self.routingManager.IsEnd(index):
            node_index = self.manager.IndexToNode(index)
            route_load += self.data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(self.data['names'][node_index], route_load)

            previous_index = index
            index = self.solution.Value(self.routingManager.NextVar(index))
            route_distance += self.routingManager.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
            print(route_distance)

        plan_output += '{0}, Load({1}) \n '.format(self.data['names'][self.manager.IndexToNode(index)], route_load)

        plan_output += 'Distance of the route: {}\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)

        print(plan_output)
        total_distance += route_distance
        total_load += route_load

    print('Total distance of all routes: {}km'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))  




if __name__ == '__main__':
  nodes = []
  vehicleNumber =2
  depotNode = 0
  
  
  vehicleS = [Vehicle(8),Vehicle(8)]

  coors = [Coors(geoString = "Ambawadi Circle, Ahmedabad"),
           Coors(geoString = "Club 07, Bopal"),
           Coors(geoString = "Naroda Patiya"),
           Coors(geoString = "The Fern Hotel, Sola"),
           Coors(geoString = "Trimandir, Adalaj")]

  demands = [0, 3, 5, 2, 6] 
  pickupNdeliveries = [[1,2]] 

  
  network =  Network(depotNode,vehicleNumber,vehicles=vehicleS, pickups_deliveries=pickupNdeliveries)

  for i in range(0, len(coors)):
    newNode = Node(coors[i], demands[i])
    network.addNodeToNetwork(newNode)

  
  print(DataModel(network).getData())

  vrp = vrpWrap(DataModel(network).getData())
  solution = vrp.solve()

  print(solution)
  print("Solution\n")
  print(vrp.print_solution())
