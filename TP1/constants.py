import numpy as np
import enum

# Matrix element values

UP=np.array([-1,0])
DOWN=np.array([1,0])
LEFT=np.array([0,-1])
RIGHT=np.array([0,1])
ALL_DIRECTIONS=[UP, RIGHT, DOWN, LEFT]

class SearchMethods(enum.Enum):
   BFS = "BFS"
   DFS = "DFS"
   IDDFS = "IDDFS"
   GREEDY = "GREEDY"
   IDA_STAR = "IDA*"
   A_STAR = "A*"

   def __str__(self):
      return str(self.value)

class ConfigOptions(enum.Enum):
   ALGORITHM = "algorithm"
   MAX_DEPTH = "maxDepth"
   HEURISTIC = "heuristic"

   def __str__(self):
      return str(self.value)

class BoardElement(enum.Enum):
   SPACE='.'
   WALL='X'
   BOX='B'
   PLAYER='O'
   GOAL='G'

   def __eq__(self, value):
      return self.value == value
   
   def __str__(self):
      return str(self.value)