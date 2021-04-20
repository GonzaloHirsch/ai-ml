# Lib imports
import csv
import time
import os
import numpy as np
import random
from sys import stdout
# Local imports
import parser
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"
OUTPUT_DIR = "output/"
OUTPUT_WEIGHTS_FIELDNAMES = ["weights"]
OUTPUT_ERRORS_FIELDNAMES = ["iteration", "error"]
weights = []
errors = []

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
def prepareOutput(filename, fields):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(filename, 'w+') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()

# Writes a row of data to the output file
def writeAllWeights(writer):
    for i in range(len(weights)):
        info = {
            OUTPUT_WEIGHTS_FIELDNAMES[0]: weights[i]
        }
        writer.writerow(info)

        # Writes a row of data to the output file
def writeAllErrors(writer):
    for i in range(len(errors)):
        info = {
            OUTPUT_ERRORS_FIELDNAMES[0]: i,
            OUTPUT_ERRORS_FIELDNAMES[1]: errors[i],
        }
        writer.writerow(info)

# -----------------------------------------------------------------
# TRAININGS
# -----------------------------------------------------------------

def getRandomDatasetOrder(datasetLength):
    return random.sample(range(0, datasetLength), datasetLength)

# ----------------------------
# SINGLE LAYER
# ----------------------------

def predict(perceptron, trainData):
    summation = perceptron.summation(trainData)
    prediction = perceptron.activate(summation)
    return summation, prediction

def testPerceptron(perceptron, trainingInput, labels, delta):
    # Get accuracy
    accuracy = 0
    for i in range(len(trainingInput)):
        summ, activ = predict(perceptron, trainingInput[i])
        # print("Input:", trainingInput[i], "Label:", labels[i], "Result:", activ, "Status:", "OK" if abs(labels[i] - activ) <= delta else "ERROR")
        accuracy += 1 if abs(labels[i] - activ) <= delta else 0
    print("Accuracy:", accuracy/trainingInput.shape[0])

def trainSingle(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create with shape because of N points of M components being NxM
    perceptron = Perceptron(trainingInput.shape[1], config.activation, config.learningRate, config.beta, config.momentum, config.alpha)
    # For graphing
    weights.append(perceptron.getWeights())

    # Define output file and prepare output
    filenameWeights = OUTPUT_DIR + ('run_input%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameErrors = OUTPUT_DIR + ('run_errors%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    prepareOutput(filenameWeights, OUTPUT_WEIGHTS_FIELDNAMES)
    prepareOutput(filenameErrors, OUTPUT_ERRORS_FIELDNAMES)

    trainingSize = trainingInput.shape[0]
    iterations = 0
    error = 1
                
    try:
        while iterations < config.iterations and error > config.error:
            stdout.write("Epoch #" + str(iterations) + "\r")
            stdout.flush()
            # Getting a random index order
            indexes = getRandomDatasetOrder(trainingSize)

            for x_i in indexes:
                # Make the prediction
                summation, prediction = predict(perceptron, trainingInput[x_i])

                # Correct Perceptron weights.
                perceptron.correctWeights(trainingInput[x_i], labels[x_i], prediction, summation)
            
            # Calculate error.
            error = 0
            for inputs, label in zip(trainingInput, labels):
                summation, prediction = predict(perceptron, inputs)
                error += perceptron.calculateError(label, prediction)

            errors.append(error[0])
            weights.append(perceptron.getWeights())

            iterations += 1

        # Write output
        with open(filenameWeights, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_WEIGHTS_FIELDNAMES)
            writeAllWeights(csv_writer)

        # Write errors
        with open(filenameErrors, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_ERRORS_FIELDNAMES)
            writeAllErrors(csv_writer)

        print("\n\n######################\nTESTING\n######################")

        print("Training Results:")
        testPerceptron(perceptron, trainingInput, labels, config.delta)

        print("Training Results:")
        testPerceptron(perceptron, trainingInputTest, labelsTest, config.delta)

        # print("Weights", perceptron.weights)
        # print("Error", error)

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
        network.append(np.array([Perceptron(weightCount, layer[0], config.learningRate, config.beta, config.momentum, config.alpha) for x in range(0, layer[1])], dtype = Perceptron))
        # Store previous layer
        lastLayer = layer
    return np.array(network, dtype = object)

# Method to forward propagate into the network
def forwardPropagate(network, trainingInput, networkSize, itemIndex):
    activationValues = []
    summationValues = []
    for index, layer in enumerate(network):
        # Get data to pass to layer, use training input or activated data before
        data = trainingInput[itemIndex] if index == 0 else activationValues[index - 1]
        # Perform all summations
        summationValues.append(np.array([perceptron.summation(data) for perceptron in layer]))
        # Perform all activations
        activations = [layer[i].activate(summationValues[index][i]) for i in range(len(summationValues[index]))]
        # If it's not the last layer, add bias to activations for next iterations
        if index < networkSize - 1:
            activations = [1] + activations
        activationValues.append(np.array(activations))
    return summationValues, activationValues

def testNetwork(network, networkSize, trainingInput, labels, delta):
    # Get accuracy
    accuracy = 0
    for i in range(len(trainingInput)):
        summ, activ = forwardPropagate(network, trainingInput, networkSize, i)
        # print("Input:", trainingInput[i], "Label:", labels[i], "Result:", activ[-1][0], "Status:", "OK" if abs(labels[i] - activ[-1][0]) <= delta else "ERROR")
        accuracy += 1 if abs(labels[i] - activ[-1][0]) <= delta else 0
    print("Accuracy:", accuracy/trainingInput.shape[0])

# Trains the multilayer network
def trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create the network dinamically
    network = createNetwork(config, trainingInput.shape[1])

    # Define output file and prepare output
    filenameErrors = OUTPUT_DIR + ('run_errors%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    prepareOutput(filenameErrors, OUTPUT_ERRORS_FIELDNAMES)

    # Store sizes to avoid multiple calls
    trainingSize = trainingInput.shape[0]
    networkSize = network.shape[0]
    iterations = 0
    error = 1
    try:
        while iterations < config.iterations and error > config.error:
            stdout.write("Epoch #" + str(iterations) + "\r")
            stdout.flush()
            
            # Getting a random index order
            indexes = getRandomDatasetOrder(trainingSize)

            for itemIndex in indexes:
            
                # Propagate
                summationValues, activationValues = forwardPropagate(network, trainingInput, networkSize, itemIndex)

                # Calculate prediction to backpropagate
                # Asume only 1 neuron in last layer and 1 result in collections
                # This is delta/phi M
                initialBackpropagation = network[-1][0].initialBackpropagate(summationValues[-1][0], labels[itemIndex], activationValues[-1][0])
                
                # Backpropagate
                # Create array of fixed size and set last value
                backpropagationValues = [None] * networkSize
                backpropagationValues[-1] = np.array([initialBackpropagation])
                # Use from size-2 to avoid out of bounds and last layer
                # Use -1 as stop to finish in layer 0 and -1 in step to go in inverse direction
                for index in range(networkSize - 2, -1, -1):
                    # Iterate each perceptron in layer
                    data = []
                    for subindex, perceptron in enumerate(network[index]):
                        # Get all weights leaving that perceptron 
                        # Add 1 to index to take into account bias
                        outboundWeights = np.array([p.weights[subindex + 1] for p in network[index + 1]])
                        # Calculate backpropagation for next layer in iteration
                        data.append(perceptron.backpropagate(summationValues[index][subindex], outboundWeights, backpropagationValues[index + 1]))
                    # Add all backpropagation values
                    backpropagationValues[index] = np.array(data)
                
                # Correct weights
                for index, layer in enumerate(network):
                    # Determine which data using depending on index
                    data = trainingInput[itemIndex] if index == 0 else activationValues[index - 1]
                    # Call weight correction on each one
                    for subindex, p in enumerate(layer):
                        p.correctHiddenWeights(backpropagationValues[index][subindex], data)

            # Calculate error once epoch is finished
            error = 0
            perceptron = network[-1][0]
            for i in range(len(trainingInput)):
                summ, activ = forwardPropagate(network, trainingInput, networkSize, i)
                error += perceptron.calculateError(labels[i], activ[-1][0])
            errors.append(error[0])

            # Increase iterations
            iterations += 1

        # Write errors
        with open(filenameErrors, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_ERRORS_FIELDNAMES)
            writeAllErrors(csv_writer)

        print("\n\n######################\nTESTING\n######################")

        print("Training Results:")
        testNetwork(network, networkSize, trainingInput, labels, config.delta)

        print("Learning Results:")
        testNetwork(network, networkSize, trainingInputTest, labelsTest, config.delta)

        # print("Error", error)

    except KeyboardInterrupt:
        print("Finishing up...")


# Parses data and triggers training
def main():
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse input
    trainingInput = parser.parseInput(config.input, addExtraInput=True, flatten=config.flatten, normalize=False)
    labels = parser.parseInput(config.desired, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)
    # Parse input test
    trainingInputTest = parser.parseInput(config.inputTest, addExtraInput=True, flatten=config.flatten, normalize=False)
    labelsTest = parser.parseInput(config.desiredTest, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)
    
    print("######################\nTRAINING\n######################")
    if config.multilayer:
        trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest)
    else:
        trainSingle(config, trainingInput, labels, trainingInputTest, labelsTest)
    

# App entrypoint
if __name__ == "__main__":
    main()