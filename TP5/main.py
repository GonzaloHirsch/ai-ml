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
from constants import ModeOptions

CONFIG_INPUT = "input/configuration.json"

# Trains the multilayer network
def trainMultilayer(config, inputs):
    # Create instance of the network
    network = Network(config, inputs.shape[1])
    # Train the network
    network.train(inputs)
    # If generator points were given
    if len(config.generatorPoints) > 0:
        results = network.generate(config.generatorPoints)
        results = [[r[0], np.array([1 if e > 0.5 else 0 for e in r[1]]).reshape((7, 5))] for r in results]
        for result in results:
            print(f'Generated using {result[0]}:\n {result[1]}')

# Trains the multilayer network
def trainMultilayerOptimizer(config, inputs, optimizer):
    # Create instance of the network
    network = Network(config, inputs.shape[1])
    # Train the network
    error = network.trainMinimizer(inputs, optimizer)
    # If generator points were given
    # if len(config.generatorPoints) > 0:
    #     results = network.generate(config.generatorPoints)
    #     results = [[r[0], np.array([1 if e > 0.5 else 0 for e in r[1]]).reshape((7, 5))] for r in results]
    #     for result in results:
    #         print(f'Generated using {result[0]}:\n {result[1]}')


# Parses data and triggers training
def main():
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse input
    inputs = parser.parseInput(config.input)

    print("######################\nTRAINING\n######################")
    if config.mode == ModeOptions.NORMAL.value:
        trainMultilayer(config, inputs)
    elif config.mode == ModeOptions.DENOISER.value:
        trainMultilayer(config, inputs)
    elif config.mode == ModeOptions.OPTIMIZER.value:
        trainMultilayerOptimizer(config, inputs, config.optimizer)
    else:
        trainMultilayer(config, inputs)
    

# App entrypoint
if __name__ == "__main__":
    main()