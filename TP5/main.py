# Lib imports
import csv
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import random
from sys import stdout
from math import floor
# Local imports
import parser
from network import Network
from constants import ModeOptions
from helper import createNoise

CONFIG_INPUT = "input/configuration.json"

def trainGenerative(config):
    # Parse input images
    inputs = parser.parseInput(config.input)
    labels = ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_']
    # Create instance of the network
    network = Network(config, inputs[0].shape[0])
    # Train the network
    network.train(inputs, inputs, labels)
    n = 25
    dimensions = (7, 5)
    grid_x = np.linspace(-1, 1, n)
    grid_y = np.linspace(-1, 1, n)
    figure = np.zeros((dimensions[0] * n, dimensions[1] * n))
    for i, yi in enumerate(grid_x):
        for j, xi in enumerate(grid_y):
            # Include bias in sample
            z_sample = np.array([1, xi, yi])
            x_decoded = network.generateFromPoint(z_sample)
            x_decoded = np.array([0 if e > 0.5 else 1 for e in x_decoded])
            digit = x_decoded.reshape(dimensions[0], dimensions[1])
            figure[i * dimensions[0]: (i + 1) * dimensions[0],
                j * dimensions[1]: (j + 1) * dimensions[1]] = digit
    plt.figure(figsize=(7, 7))
    plt.imshow(figure, cmap='Greys_r')
    plt.show()

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

    print("######################\nTRAINING\n######################")
    if config.mode == ModeOptions.NORMAL.value:
        # Parse input
        inputs = parser.parseInput(config.input)
        trainMultilayer(config, inputs)
    elif config.mode == ModeOptions.DENOISER.value:
        # Parse input
        inputs = parser.parseInput(config.input)
        trainDenoiser(config, inputs)
    elif config.mode == ModeOptions.OPTIMIZER.value:
        # Parse input
        inputs = parser.parseInput(config.input)
        trainMultilayerOptimizer(config, inputs, config.optimizer)
    else:
        trainGenerative(config)
    

# App entrypoint
if __name__ == "__main__":
    main()