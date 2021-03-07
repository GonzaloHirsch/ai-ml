from numpy import random
import numpy as np
from constants import BoardElement
from constants import SearchMethods

# Name of the configuration file with the inner configuration
def generateMatrixAndPositions(filename):

    f = open(filename, "r")

    matrix = []
    playerPosition = []
    boxesPositions = []
    targetPositions = []

    rowIdx = 0

    for line in f:
        row = [x for x in line.rstrip("\n").split(" ")]

        for colIdx in range(0, len(row)):

            element = row[colIdx]

            if element == BoardElement.PLAYER:
                playerPosition = np.array([rowIdx, colIdx])

            elif element == BoardElement.BOX:
                boxesPositions.append(np.array([rowIdx, colIdx]))

            elif element == BoardElement.GOAL:
                targetPositions.append(np.array([rowIdx, colIdx]))

            if element == BoardElement.PLAYER or element == BoardElement.BOX:
                row[colIdx] = BoardElement.SPACE.value

        if rowIdx == 0:
            matrix = np.array(row)
        else:
            matrix = np.vstack((matrix, row))

        rowIdx += 1

    boxesPositions = np.array(boxesPositions)
    targetPositions = np.array(targetPositions)

    return matrix, boxesPositions, targetPositions, playerPosition


def generateConfigDetails(configFile):

    f = open(configFile, "r")

    index = 0
    maxDepth = 1

    for line in f:
        if index == 0:
            algorithm = line.rstrip("\n")
        if algorithm == SearchMethods.IDDFS.name and index == 1:
            maxDepth = int(line.rstrip("\n"))
        
        index += 1

    return algorithm, maxDepth





    

    

