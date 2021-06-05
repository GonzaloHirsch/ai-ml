from random import sample
from sys import stdout
from numpy import matrix, savetxt
import os

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
def writeMatrixToFile(filename, _matrix):
    mat = matrix(_matrix)
    with open(OUTPUT_DIR + filename,'wb') as f:
        for line in mat:
            savetxt(f, line, fmt='%.2f')

# Creates a directory if the directory doesn't exist
def createDirectoryIfNotExist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)