from numpy import random
import numpy as np
from constants import BoardElement
from constants import SearchMethods
from constants import ConfigOptions
from config import Config
import json

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
    with open(configFile) as json_file:
        data = json.load(json_file)
        if data[ConfigOptions.ALGORITHM.value] == SearchMethods.A_STAR.value or data[ConfigOptions.ALGORITHM.value] == SearchMethods.GREEDY.value or data[ConfigOptions.ALGORITHM.value] == SearchMethods.IDA_STAR.value:
            return Config(data[ConfigOptions.ALGORITHM.value], heuristic=data[ConfigOptions.HEURISTIC.value])
        elif data[ConfigOptions.ALGORITHM.value] == SearchMethods.IDDFS.value or data[ConfigOptions.ALGORITHM.value] == SearchMethods.IDDFS_PRUNING.value:
            return Config(data[ConfigOptions.ALGORITHM.value], maxDepth=data[ConfigOptions.MAX_DEPTH.value])
        else:
            return Config(data[ConfigOptions.ALGORITHM.value])
