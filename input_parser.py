from numpy import random
import numpy as np
import constants

# Name of the configuration file with the inner configuration
INPUT_CONFIGURATION_FILE = "./examples/boards.txt"


def generate_matrix(filename):

    f = open(filename, "r")

    matrix = []

    index = 0
    for line in f:
        row = [int(x) for x in line.rstrip("\n").split(" ")]

        if index == 0:
            matrix = np.array(row)

        for idx in range(0, len(row)):
            if row[idx] == constants.WALL or row[idx] == constants.USER:
                row[idx] == constants.SPACE

        matrix = np.vstack((matrix, row))

        index += 1

    return matrix


print(generate_matrix(INPUT_CONFIGURATION_FILE))
