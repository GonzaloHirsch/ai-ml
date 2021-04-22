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
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"
OUTPUT_DIR = "output/"
OUTPUT_WEIGHTS_FIELDNAMES = ["weights"]
OUTPUT_ERRORS_FIELDNAMES = ["iteration", "error"]
OUTPUT_METRICS_FIELDNAMES = ["iteration", "accuracy", "precision_T", "precision_F", "recall_T", "recall_F", "f1_T", "f1_F"]
OUTPUT_ACCURACY_FIELDNAMES = ["iteration", "accuracy"]
weights = []
errors = []
trainMetrics = []
testMetrics = []

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

def printMetrics(accuracy, precision = None, recall = None, f1 = None):
    print("Accuracy:", accuracy)
    if precision != None:
        print(('Data for 1:\n\tPrecision: %s\n\tRecall: %s\n\tF1_score: %s' % (precision[1], recall[1], f1[1])))
        print(('Data for -1:\n\tPrecision: %s\n\tRecall: %s\n\tF1_score: %s' % (precision[-1], recall[-1], f1[-1])))

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

def writeAllMetrics(writer, metrics):
    for i in range(len(metrics)):
        m = metrics[i]
        info = {
            OUTPUT_METRICS_FIELDNAMES[0]: i,
            OUTPUT_METRICS_FIELDNAMES[1]: m[0],
            OUTPUT_METRICS_FIELDNAMES[2]: m[1][1],
            OUTPUT_METRICS_FIELDNAMES[3]: m[1][-1],
            OUTPUT_METRICS_FIELDNAMES[4]: m[2][1],
            OUTPUT_METRICS_FIELDNAMES[5]: m[2][-1],
            OUTPUT_METRICS_FIELDNAMES[6]: m[3][1],
            OUTPUT_METRICS_FIELDNAMES[7]: m[3][-1],
        }
        writer.writerow(info)

def writeAccuracyMetrics(writer, metrics):
    for i in range(len(metrics)):
        m = metrics[i]
        info = {
            OUTPUT_ACCURACY_FIELDNAMES[0]: i,
            OUTPUT_ACCURACY_FIELDNAMES[1]: m[0],
        }
        writer.writerow(info)

# -----------------------------------------------------------------
# TRAININGS
# -----------------------------------------------------------------

def getRandomDatasetOrder(datasetLength):
    return random.sample(range(0, datasetLength), datasetLength)

def getMetrics(labels, results, delta, calculateMetrics = True):
    # Predictions that were right and wrong
    truePredictions = {1: 0, -1: 0}
    # If label is 1 and result is -1, falsePredictions[1]++, it will store false
    # Results for other label
    falsePredictions = {1: 0, -1: 0}
    expectedPredictions = {1: 0, -1: 0}
    accuracy = 0
    # Prepare structures for metrics
    for i in range(len(labels)):
        label = labels[i][0]
        # Count number of predictions in each that is expected
        if calculateMetrics:
            expectedPredictions[label] += 1
        # If prediction is correct
        if abs(label - results[i]) <= delta:
            accuracy += 1
            if calculateMetrics:
                truePredictions[label] += 1
        else:
            if calculateMetrics:
                falsePredictions[label] += 1
    # Calculate metrics
    accuracy = accuracy / len(labels)
    if calculateMetrics:
        precision = {}
        recall = {}
        f1 = {}
        # Asumes labels and keys are 1 and -1, interchangeable by multiplying by -1
        for key in truePredictions:
            # Initiate
            precision[key] = truePredictions[key]/((truePredictions[key] + falsePredictions[key * -1]) if (truePredictions[key] + falsePredictions[key * -1]) > 0 else 1)
            recall[key] = truePredictions[key]/(expectedPredictions[key] if expectedPredictions[key] > 0 else 1)
            f1[key] = (2 * precision[key] * recall[key])/((precision[key] + recall[key]) if (precision[key] + recall[key]) > 0 else 1)
        return accuracy, precision, recall, f1
    return accuracy, None, None, None


# ----------------------------
# SINGLE LAYER
# ----------------------------

def predict(perceptron, trainData):
    summation = perceptron.summation(trainData)
    prediction = perceptron.activate(summation)
    return summation, prediction

def testPerceptron(perceptron, trainingInput, labels, delta, printData = False, calculateMetrics = True):
    # Get accuracy
    activations = []
    for i in range(len(trainingInput)):
        summ, activ = predict(perceptron, trainingInput[i])
        if printData:
            print("Input:", trainingInput[i], "Label:", labels[i], "Result:", activ, "Status:", "OK" if abs(labels[i] - activ) <= delta else "ERROR")
        activations.append(activ)
    # Get metrics
    accuracy, precision, recall, f1 = getMetrics(labels, activations, delta, calculateMetrics)
    return accuracy, precision, recall, f1

def trainSingle(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create with shape because of N points of M components being NxM
    perceptron = Perceptron(trainingInput.shape[1], config.activation, config.learningRate, config.beta, config.momentum, config.alpha)
    # For graphing
    weights.append(perceptron.getWeights())

    # Define output file and prepare output
    filenameWeights = OUTPUT_DIR + ('run_input%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameErrors = OUTPUT_DIR + ('run_errors%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameTrain = OUTPUT_DIR + ('run_train%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameTest = OUTPUT_DIR + ('run_test%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    prepareOutput(filenameWeights, OUTPUT_WEIGHTS_FIELDNAMES)
    prepareOutput(filenameErrors, OUTPUT_ERRORS_FIELDNAMES)
    prepareOutput(filenameTrain, OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
    prepareOutput(filenameTest, OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)

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

            # Calculate metrics
            accuracy, precision, recall, f1 = testPerceptron(perceptron, trainingInput, labels, config.delta, calculateMetrics=config.calculateMetrics)
            trainMetrics.append([accuracy, precision, recall, f1] if config.calculateMetrics else [accuracy])
            accuracy, precision, recall, f1 = testPerceptron(perceptron, trainingInputTest, labelsTest, config.delta, calculateMetrics=config.calculateMetrics)
            testMetrics.append([accuracy, precision, recall, f1] if config.calculateMetrics else [accuracy])

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
        accuracy, precision, recall, f1 = testPerceptron(perceptron, trainingInput, labels, config.delta, True, calculateMetrics=config.calculateMetrics)
        printMetrics(accuracy, precision, recall, f1)
        with open(filenameTrain, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
            if config.calculateMetrics:
                writeAllMetrics(csv_writer, trainMetrics)
            else:
                writeAccuracyMetrics(csv_writer, trainMetrics)

        print("Learning Results:")
        accuracy, precision, recall, f1 = testPerceptron(perceptron, trainingInputTest, labelsTest, config.delta, True, calculateMetrics=config.calculateMetrics)
        printMetrics(accuracy, precision, recall, f1)
        with open(filenameTest, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
            if config.calculateMetrics:
                writeAllMetrics(csv_writer, testMetrics)
            else:
                writeAccuracyMetrics(csv_writer, testMetrics)

        # print("Weights", perceptron.weights)
        print("Error", error)

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

def testNetwork(network, networkSize, trainingInput, labels, delta, printData = False, calculateMetrics = True):
    # Get accuracy
    accuracy = 0
    activations = []
    for i in range(len(trainingInput)):
        summ, activ = forwardPropagate(network, trainingInput, networkSize, i)
        if printData:
            print("Input:", trainingInput[i], "Label:", labels[i], "Result:", activ[-1][0], "Status:", "OK" if abs(labels[i] - activ[-1][0]) <= delta else "ERROR")
        activations.append(activ[-1][0])
    # Get metrics
    accuracy, precision, recall, f1 = getMetrics(labels, activations, delta, calculateMetrics)
    return accuracy, precision, recall, f1

# Trains the multilayer network
def trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest):
    # Create the network dinamically
    network = createNetwork(config, trainingInput.shape[1])

    # Define output file and prepare output
    filenameErrors = OUTPUT_DIR + ('run_errors%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameTrain = OUTPUT_DIR + ('run_train%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    filenameTest = OUTPUT_DIR + ('run_test%s_%s_%s_%s.csv' % (trainingInput.shape[0], config.activation, config.learningRate, time.time()))
    prepareOutput(filenameErrors, OUTPUT_ERRORS_FIELDNAMES)
    prepareOutput(filenameTrain, OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
    prepareOutput(filenameTest, OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)

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

            # Calculate metrics
            # Train metrics
            accuracy, precision, recall, f1 = testNetwork(network, networkSize, trainingInput, labels, config.delta, calculateMetrics=config.calculateMetrics)
            trainMetrics.append([accuracy, precision, recall, f1] if config.calculateMetrics else [accuracy])
            # Test metrics
            accuracy, precision, recall, f1 = testNetwork(network, networkSize, trainingInputTest, labelsTest, config.delta, calculateMetrics=config.calculateMetrics)
            testMetrics.append([accuracy, precision, recall, f1] if config.calculateMetrics else [accuracy])

            # Increase iterations
            iterations += 1

        # Write errors
        with open(filenameErrors, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_ERRORS_FIELDNAMES)
            writeAllErrors(csv_writer)

        print("\n\n######################\nTESTING\n######################")

        print("Training Results:")
        accuracy, precision, recall, f1 = testNetwork(network, networkSize, trainingInput, labels, config.delta, printData=True, calculateMetrics=config.calculateMetrics)
        printMetrics(accuracy, precision, recall, f1)
        with open(filenameTrain, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
            if config.calculateMetrics:
                writeAllMetrics(csv_writer, trainMetrics)
            else:
                writeAccuracyMetrics(csv_writer, trainMetrics)

        print("Learning Results:")
        accuracy, precision, recall, f1 = testNetwork(network, networkSize, trainingInputTest, labelsTest, config.delta, printData=True, calculateMetrics=config.calculateMetrics)
        printMetrics(accuracy, precision, recall, f1)
        with open(filenameTest, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_METRICS_FIELDNAMES if config.calculateMetrics else OUTPUT_ACCURACY_FIELDNAMES)
            if config.calculateMetrics:
                writeAllMetrics(csv_writer, testMetrics)
            else:
                writeAccuracyMetrics(csv_writer, testMetrics)

        print("Error", error)

    except KeyboardInterrupt:
        print("Finishing up...")


# Parses data and triggers training
def main():
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse input
    inputs = parser.parseInput(config.input, addExtraInput=True, flatten=config.flatten, normalize=False)
    labels = parser.parseInput(config.desired, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)
    
    if config.useKTraining:
        # block size of the test data
        blockSize = floor(len(inputs)/config.blockAmount)
        # start and end indexes of the test data
        startTestIdx = config.testBlock * blockSize
        endTestIdx = startTestIdx + blockSize
        # if the end exceeds the range (due to uneven block size)
        if (endTestIdx > len(inputs)):
            endTestIdx = len(inputs)
        # Indexes of the test data
        testIdxs = np.arange(startTestIdx, endTestIdx)

        # Training data
        trainingInputs = np.delete(inputs, testIdxs, axis=0) # 0 indicates to delete row
        trainingLabels = np.delete(labels, testIdxs, axis=0) 

        # Test data
        testInputs = inputs[startTestIdx:endTestIdx]
        testLabels = labels[startTestIdx:endTestIdx]
    else:
        trainingInputs = inputs
        trainingLabels = labels
        # Parse input test
        testInputs = parser.parseInput(config.inputTest, addExtraInput=True, flatten=config.flatten, normalize=False)
        testLabels = parser.parseInput(config.desiredTest, addExtraInput=False, flatten=1, normalize=config.normalizeDesired)

    print("######################\nTRAINING\n######################")
    if config.multilayer:
        trainMultilayer(config, trainingInputs, trainingLabels, testInputs, testLabels)
    else:
        trainSingle(config, trainingInputs, trainingLabels, testInputs, testLabels)
    

# App entrypoint
if __name__ == "__main__":
    main()