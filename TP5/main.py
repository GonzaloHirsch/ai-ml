# Lib imports
import csv
import time
import os
import numpy as np
import random
from sys import stdout
from math import floor
# Local imports
import parser
from network import Network

CONFIG_INPUT = "input/configuration.json"

# Trains the multilayer network
def trainMultilayer(config, inputs):
    # Create instance of the network
    network = Network(config, inputs.shape[1])
    # Train the network
    network.train(inputs)

# Parses data and triggers training
def main():
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse input
    # inputs = parser.parseInput(config.input, addExtraInput=True)
    inputs = np.array([[1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1]])

    print("######################\nTRAINING\n######################")
    trainMultilayer(config, inputs)
    

# App entrypoint
if __name__ == "__main__":
    main()