from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import time
import math
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix


def calculateDistance(coor1, coor2):
  return math.sqrt((coor1.x-coor2.x)**2 + (coor1.y-coor2.y)**2)

  

class Node:
  def __init__(self, x,y):
    self.x = x
    self.y = y
  
class DataModel:
  def __init__(self, nodes):
    self.data = {}
    self.nodes = nodes 


  def calculateDistanceMatrix(self):
    df = pd.DataFrame(nodes, columns=['xcord', 'ycord'])
    return pd.DataFrame(distance_matrix(df.values, df.values))

  

if __name__ == '__main__':
  nodes = []

  nodes.append((5, 7))
  nodes.append((7, 3))
  nodes.append((8, 2))



  nodes = np.array(nodes)
  print(type(nodes))


  print(DataModel(nodes).calculateDistanceMatrix())

