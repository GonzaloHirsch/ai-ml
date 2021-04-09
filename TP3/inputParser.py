# Lib imports
import numpy as np
# Local imports

# Function to parse a file and split and store contents
# Returns a np.array with all data
def parseInput(filepath):
    with open(filepath) as f:
        # Read all lines
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(np.array([float(elem) for elem in line.strip().split()]))
    return np.array(data)


print(parseInput("datasets/TP3-ej2-Conjuntoentrenamiento.txt"))