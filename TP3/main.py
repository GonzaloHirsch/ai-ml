# Lib imports
import csv
import time
import os
import numpy as np
import random
# Local imports
import parser
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"
OUTPUT_DIR = "output/"
OUTPUT_FIELDNAMES = ["weights"]
weights = []

# -----------------------------------------------------------------
# DEBUG METHODS
# -----------------------------------------------------------------

def printNetwork(network):
    count = 0
    for layer in network:
        print("LAYER #" + str(count))
        for p in layer:
            print(p)
        count += 1

# -----------------------------------------------------------------
# FILE WRITING
# -----------------------------------------------------------------

# Makes sure the CSV file is prepared, create it if non existent
def prepareOutput(filename):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(filename, 'w+') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
        csv_writer.writeheader()

# Writes a row of data to the output file
def writeAll(writer):
    for i in range(len(weights)):
        info = {
            OUTPUT_FIELDNAMES[0]: weights[i],
        }
        writer.writerow(info)

# -----------------------------------------------------------------
# TRAININGS
# -----------------------------------------------------------------

# ----------------------------
# SINGLE LAYER
# ----------------------------

def trainSingle(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create with shape because of N points of M components being NxM
    perceptron = Perceptron(trainingInput.shape[1], config.activation, config.learningRate)
    # For graphing
    weights.append(perceptron.getWeights())

    # Define output file and prepare output
    filename = OUTPUT_DIR + ('run_input%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    prepareOutput(filename)

    iterations = 0
    error = 1
                
    try:
        while iterations < config.iterations and error > config.error:
            print("Iteration #" + str(iterations))
            x_i = random.randint(0,trainingInput.shape[0] - 1)

            summation = perceptron.summation(trainingInput[x_i])
            prediction = perceptron.activate(summation)

            # Correct Perceptron weights.
            perceptron.correctWeights(trainingInput[x_i], labels[x_i], prediction, summation)
            
            # Calculate error.
            error = 0
            for inputs, label in zip(trainingInput, labels):
                summation = perceptron.summation(inputs)
                prediction = perceptron.activate(summation)
                error += perceptron.calculateError(label, prediction)


            weights.append(perceptron.getWeights())
            print("Weights", perceptron.weights)
            print("Error", error)

            iterations += 1

        # Write output
        with open(filename, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
            writeAll(csv_writer)

    except KeyboardInterrupt:
        print("Finishing up...")

# ----------------------------
# MULTI LAYER
# ----------------------------

# Dinamically builds a network
# Receives:
#   config --> Config object
#   inputSize --> Number of inputs per training point with bias taken into account
def createNetwork(config, inputSize):
    network = []
    isFirst = True
    lastLayer = []
    for layer in config.layers:
        # If its the first layer, the bias is accounted in the input size
        if isFirst:
            weightCount = inputSize
            # Modify first flag
            isFirst = False
        # If its another layer, the weights are the number of 
        # perceptrons in previous layer + 1 (bias)
        else:
            weightCount = lastLayer[1] + 1
        # layer[0] = activation, layer[1] = perceptron count
        network.append(np.array([Perceptron(weightCount, layer[0], config.learningRate) for x in range(0, layer[1])], dtype = Perceptron))
        # Store previous layer
        lastLayer = layer
    return np.array(network, dtype = object)

# Trains the multilayer network
def trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create the network dinamically
    network = createNetwork(config, trainingInput.shape[1])

    # Store sizes to avoid multiple calls
    trainingSize = trainingInput.shape[0]
    networkSize = network.shape[0]
    # Store an enumerate to avoid multiple operations
    networkEnumerate = enumerate(network)
    iterations = 0
    error = 1
    try:
        while iterations < config.iterations and error > config.error:
            print("Iteration #" + str(iterations))
            # Picking random item
            itemIndex = int(random.uniform(0, trainingSize))
            # Propagate
            activationValues = []
            summationValues = []
            for index, layer in networkEnumerate:
                # Get data to pass to layer, use training input or activated data before
                data = trainingInput[itemIndex] if index == 0 else activationValues[index - 1]
                # Perform all summations
                summationValues.append(np.array([p.summation(data) for p in layer]))
                # Perform all activations
                activations = [layer[i].activate(summationValues[index][i]) for i in range(len(summationValues[index]))]
                # If it's not the last layer, add bias to activations for next iterations
                if index < networkSize - 1:
                    activations = [1] + activations
                activationValues.append(np.array(activations))
                
            print(summationValues)
            print(activationValues)
            # Backpropagate
            # summation = perceptron.summation(inputs)

            # prediction = perceptron.activate(summation)

            # perceptron.correctWeights(inputs, label, prediction, summation)

            # error = perceptron.calculateError(label, prediction)
            iterations += 1

        print("Weights", perceptron.weights)
        print("Error", error)

    except KeyboardInterrupt:
        print("Finishing up...")


# Parses data and triggers training
def main():
    print("Parsing input data...")
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse input
    trainingInput = parser.parseInput(config.input, addExtraInput=True, flatten=config.flatten, normalize=False)
    labels = parser.parseInput(config.desired, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)
    # Parse input test
    trainingInputTest = parser.parseInput(config.inputTest, addExtraInput=True, flatten=config.flatten, normalize=False)
    labelsTest = parser.parseInput(config.desiredTest, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)
    
    if config.multilayer:
        trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest)
    else:
        trainSingle(config, trainingInput, labels, trainingInputTest, labelsTest)
    

# App entrypoint
if __name__ == "__main__":
    main()