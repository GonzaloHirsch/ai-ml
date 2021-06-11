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
from vaeNetwork import VaeNetwork
from constants import ModeOptions
from helper import createNoise

CONFIG_INPUT = "input/configuration.json"

def trainVae(config, inputs):
    # Create instance of the network
    network = VaeNetwork(config, inputs.shape[1])
    # Train the network
    network.train(inputs)
    # If generator points were given
    # if len(config.generatorPoints) > 0:
    #     results = network.generate(config.generatorPoints)
    #     results = [[r[0], np.array([1 if e > 0.5 else 0 for e in r[1]]).reshape((7, 5))] for r in results]
    #     for result in results:
    #         print(f'Generated using {result[0]}:\n {result[1]}')

# Trains the multilayer network
def trainMultilayer(config, inputs):
    # Create instance of the network
    network = Network(config, inputs.shape[1])
    # Train the network
    network.train(inputs, inputs)
    # If generator points were given
    if len(config.generatorPoints) > 0:
        results = network.generate(config.generatorPoints)
        results = [[r[0], np.array([1 if e > 0.5 else 0 for e in r[1]]).reshape((7, 5))] for r in results]
        for result in results:
            print(f'Generated using {result[0]}:\n {result[1]}')
    
    return network

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

def trainDenoiser(config, inputs):
    # Which inputs to use to generate noise
    inputsCount = len(inputs);
    indexes = [ x for x in range(0, inputsCount) ]
    indexesSample = random.sample(indexes, config.noiseCount if config.noiseCount < inputsCount else inputsCount)
    # Expected outcome 
    expected = np.array([inputs[index] for index in indexesSample])
    # Create noise with expected input
    noiseInput = np.array([createNoise(origInput, config.noiseProbability) for origInput in expected])
    
    for i in range(0, len(indexesSample)):
        print('Original Input:')
        print(expected[i][1:].reshape((7, 5)))
        print('Noise Input')
        print(noiseInput[i][1:].reshape((7, 5)))

    # Create instance of the network
    network = Network(config, inputs.shape[1])
    # Train with noise
    network.train(noiseInput, expected)


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
        trainDenoiser(config, inputs)
    elif config.mode == ModeOptions.OPTIMIZER.value:
        trainMultilayerOptimizer(config, inputs, config.optimizer)
    else:
        trainVae(config, inputs)
    

# App entrypoint
if __name__ == "__main__":
    main()