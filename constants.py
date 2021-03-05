import numpy as np

# Matrix element values
SPACE='.'
WALL='X'
BLOCK='B'
USER='O'
GOAL='G'

UP=np.array([-1,0])
DOWN=np.array([1,0])
LEFT=np.array([0,-1])
RIGHT=np.array([0,1])
ALL_DIRECTIONS=[UP, RIGHT, DOWN, LEFT]