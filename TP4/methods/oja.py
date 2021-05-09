# Lib imports
from numpy import sqrt, sum, dot
from pandas import DataFrame
# Local imports
from helper import printIterationsInPlace, getRandomDatasetOrder
from neurons.ojaNeuron import OjaNeuron

def apply(config, inputs):
    # Number of epochs that went by
    # Number of rows in the input
    epochs, numberOfRows = 0, inputs.shape[0]
    # Creating the neuron
    neuron = OjaNeuron(inputs.shape[1], config.learningRate)
    try:
        while epochs < config.iterations:
            # Printing the iteration number nicely
            printIterationsInPlace(epochs)
            # Getting a random index order
            indexes = getRandomDatasetOrder(numberOfRows)
            # Iterate indexes in given order
            for i in indexes:
                # Get chosen row
                inputRow = inputs[i]
                # Calculate summation
                summation = neuron.summation(inputRow)
                # Update weights
                neuron.correctWeights(summation, inputRow)
            epochs += 1
        # Calculate the PC1
        weights = neuron.getWeights()
        norm = sqrt(sum(dot(weights, weights)))
        df = DataFrame(data = weights/norm, columns = ['Eigenvector Approximation'])
        print(df)

    except KeyboardInterrupt:
        print("Finishing up...")