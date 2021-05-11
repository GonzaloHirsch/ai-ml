from random import sample
from sys import stdout
import numpy as np

OUTPUT_DIR = 'output/'

# Returns a random dataset index order based on the dataset length
# Input: number of rows or items in dataset
# Returs: array of mixed indexes
def getRandomDatasetOrder(datasetLength):
    return sample(range(0, datasetLength), datasetLength)

# Prints the iterations in place, creating an iteration counter
# Input: curent iteration number
def printIterationsInPlace(iterations):
    stdout.write("Epoch #{}\r".format(iterations))
    stdout.flush()

# Writes matrix to file 
# Input: file where to write, matrix to write
def writeMatrixToFile(filename, matrix):
    mat = np.matrix(matrix)
    with open(OUTPUT_DIR + filename,'wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.2f')