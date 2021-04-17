import csv
import time
import os

import parser
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"
OUTPUT_DIR = "output/"
OUTPUT_FIELDNAMES = ["weights"]
weights = []

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
            for inputs, label in zip(trainingInput, labels):
                summation = perceptron.summation(inputs)

                prediction = perceptron.activate(summation)

                perceptron.correctWeights(inputs, label, prediction, summation)

                error = perceptron.calculateError(label, prediction)
            iterations += 1

            weights.append(perceptron.getWeights())
            print("Weights", perceptron.weights)
            print("Error", error)

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

def trainMultilayer(config, trainingInput, labels, trainingInputTest, labelsTest):
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
            for inputs, label in zip(trainingInput, labels):
                summation = perceptron.summation(inputs)

                prediction = perceptron.activate(summation)

                perceptron.correctWeights(inputs, label, prediction, summation)

                error = perceptron.calculateError(label, prediction)
            iterations += 1

            weights.append(perceptron.getWeights())
            print("Weights", perceptron.weights)
            print("Error", error)

        # Write output
        with open(filename, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
            writeAll(csv_writer)

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