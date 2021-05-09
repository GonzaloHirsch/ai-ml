from random import sample
from sys import stdout

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
