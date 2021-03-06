from numpy import random
import numpy as np
from constants import BoardElement


# Name of the configuration file with the inner configuration
def generateMatrixAndPositions(filename):

    f = open(filename, "r")

    matrix = []
    playerPosition = []
    boxesPositions = np.zeros(shape=(2,2))
    targetPositions = np.zeros(shape=(2,2))

    boxIdx = 0
    rowIdx = 0
    targetIdx = 0

    for line in f:
        row = [x for x in line.rstrip("\n").split(" ")]

        for colIdx in range(0, len(row)):

            element = row[colIdx]

            if element == BoardElement.PLAYER:
                playerPosition = [rowIdx, colIdx]

            if element == BoardElement.BOX:
                boxesPositions[boxIdx] = [rowIdx, colIdx]
                boxIdx += 1

            if element == BoardElement.GOAL:
                targetPositions[targetIdx] = [rowIdx, colIdx]
                targetIdx += 1

        if rowIdx == 0:
            matrix = np.array(row)
        else:
            matrix = np.vstack((matrix, row))

        rowIdx += 1

    return matrix, boxesPositions, targetPositions, playerPosition


def generateConfigDetails(configFile):

    f = open(configFile, "r")

    index = 0

    for line in f:
        if index == 0:
            algorithm = line.rstrip("\n")
        
        index += 1

    return algorithm





    

    

