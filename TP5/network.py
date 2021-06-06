# Lib imports
import numpy as np
# Local imports
from perceptron import Perceptron
from helper import printIterationsInPlace, getRandomDatasetOrder


class Network:
    """Class to represent a Neural Network made of Perceptrons and the methods to train and predict with it
    """

    def __init__(self, config, inputSize):
        # Create the network
        self.network = self.__createNetwork(config, inputSize)
        # Store size to access it only once
        self.networkSize = self.network.shape[0]
        # Store config
        self.config = config

    def __createNetwork(self, config, inputSize):
        """Method to dynamically build the network

        Parameters:
            config --> Config object from file configuration

            inputSize --> Number of inputs per training point with bias taken into account
        Returns:
            np.array of np.array of perceptrons, each array is one layer of perceptrons
        """
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
            network.append(np.array([Perceptron(weightCount, layer[0], config.learningRate, config.beta,
                           config.momentum, config.alpha) for x in range(0, layer[1])], dtype=Perceptron))
            # Store previous layer
            lastLayer = layer
        return np.array(network, dtype=object)

    def __forwardPropagate(self, input):
        """Method to forward propagate an input to obtain a prediction from the network

        Parameters:
            input --> Input point (with bias) to be forwarded
        Returns:
            summationValues --> np.array of np.array of the different summation values calculated

            activationValues --> np.array of np.array of the different activation values calculated, the last array is the prediction
        """
        activationValues = []
        summationValues = []
        for index, layer in enumerate(self.network):
            # Get data to pass to layer, use training input or activated data before
            data = input if index == 0 else activationValues[index - 1]
            # Perform all summations
            summationValues.append(
                np.array([perceptron.summation(data) for perceptron in layer]))
            # Perform all activations
            activations = [layer[i].activate(
                summationValues[index][i]) for i in range(len(summationValues[index]))]
            # If it's not the last layer, add bias to activations for next iterations
            if index < self.networkSize - 1:
                activations = [1] + activations
            activationValues.append(np.array(activations))
        return summationValues, activationValues

    def __backPropagate(self, input, summations, activations):
        """Method to backpropagate error into the network

        Parameters:
            input --> Input point (with bias) to be forwarded

            summations --> Summation values calculated through the forward propagation

            activations --> Activation values calculated through the forward propagation
        Returns:
            backpropagationValues --> np.array of np.array of the different backpropagation values calculated
        """
        # Calculate prediction to backpropagate
        # This is delta/phi M
        # Calculate the initial backpropagation for each of the end neurons
        initialBackpropagation = [perceptron.initialBackpropagate(
            summations[-1][index], input[index], activations[-1][index]) for index, perceptron in enumerate(self.network[-1])]
        # Backpropagate
        # Create array of fixed size and set last value
        backpropagationValues = [None] * self.networkSize
        backpropagationValues[-1] = np.array(initialBackpropagation)
        # Use from size-2 to avoid out of bounds and last layer
        # Use -1 as stop to finish in layer 0 and -1 in step to go in inverse direction
        for index in range(self.networkSize - 2, -1, -1):
            # Iterate each perceptron in layer
            data = []
            for subindex, perceptron in enumerate(self.network[index]):
                # Get all weights leaving that perceptron
                # Add 1 to index to take into account bias
                outboundWeights = np.array(
                    [p.weights[subindex + 1] for p in self.network[index + 1]])
                # Calculate backpropagation for next layer in iteration
                data.append(perceptron.backpropagate(
                    summations[index][subindex], outboundWeights, backpropagationValues[index + 1]))
            # Add all backpropagation values
            backpropagationValues[index] = np.array(data)
        return backpropagationValues

    def __correctWeights(self, input, backpropagations, activations):
        """Method to corrects weights through the network

        Parameters:
            input --> Input point (with bias) to be forwarded

            backpropagations --> Backpropagation values calculated through the backpropagation

            activations --> Activation values calculated through the forward propagation
        Returns:
            Nothing, it updates the values across the network
        """
        # Correct weights
        for index, layer in enumerate(self.network):
            # Determine which data using depending on index
            data = input if index == 0 else activations[index - 1]
            # Call weight correction on each one
            for subindex, p in enumerate(layer):
                p.correctHiddenWeights(backpropagations[index][subindex], data)

    def __computeInputError(self, actualData, predictedData):
        """Method to compute the ||X-X'||^2 distance error

        Parameters:
            actualData --> Expected data

            predictedData --> Predicted data
        Returns:
            Float, error calculated
        """
        return np.linalg.norm(actualData-predictedData)**2

    def __calculateError(self, input, expected):
        """Method to calculate the error of the network

        Parameters:
            input --> All the input points

            expected --> All the expected values for those input points
        Returns:
            Float, error calculated across the network
        """
        error = 0
        for i in range(len(input)):
            # Propagate to get the last activation value
            _, activ = self.__forwardPropagate(input[i])
            print(expected[i][1:], activ[-1])
            error += self.__computeInputError(expected[i][1:], activ[-1])
        return error

    def predict(self, input):
        """Method to calculate a prediction given the input

        Parameters:
            input --> Value to predict from
        Returns:
            np.array with the predicted value
        """
        _, activ = self.__forwardPropagate(input)
        return activ[-1]

    def train(self, input):
        """Method to train the neural network instance based on a training input set

        Parameters:
            input --> Values to train the network with
        Returns:
            Nothing, it trains the network
        """
        trainingSize = input.shape[0]
        iterations = 0
        error = 1
        errors = []
        try:
            # Iterate while iterations less than config and error less than config
            while iterations < self.config.iterations and error > self.config.error:
                # Print the iteration number in place
                printIterationsInPlace(iterations)
                # Getting a random index order
                indexes = getRandomDatasetOrder(trainingSize)
                # Iterate through the dataset order
                for itemIndex in indexes:
                    # Forward propagation
                    summationValues, activationValues = self.__forwardPropagate(
                        input[itemIndex])
                    # Backpropagation
                    backpropagationValues = self.__backPropagate(
                        input[itemIndex], summationValues, activationValues)
                    # Weight correction
                    self.__correctWeights(
                        input[itemIndex], backpropagationValues, activationValues)
                # Calculate error once epoch is finished
                error = self.__calculateError(input, input)
                errors.append(error)
                # Increment iterations
                iterations += 1
            print(errors)
        except KeyboardInterrupt:
            print("Finishing up...")
