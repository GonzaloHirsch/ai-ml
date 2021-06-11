# Lib imports
import numpy as np
from scipy.optimize import minimize
# Local imports
from perceptron import Perceptron
from helper import printIterationsInPlace, getRandomDatasetOrder
from graphing import plotLatentSpace

class Network:
    """Class to represent a Neural Network made of Perceptrons and the methods to train and predict with it
    """

    def __init__(self, config, inputSize):
        # Dimension of the input
        self.inputSize = inputSize
        # Create the network
        self.network = self.__createNetwork(config, inputSize)
        # Store size to access it only once
        self.networkSize = self.network.shape[0]
        # Store config
        self.config = config
        # Latent code data
        self.latentCode = []

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

    def __flattenNetwork(self):
        weightMatrix = []
        # Matrix with all the weights as rows
        for layer in self.network:
            for perceptron in layer:
                weightMatrix.append(perceptron.getWeights()) 
        
        weightMatrix = np.array(weightMatrix, dtype=object)
        # Flatten the weights matrix to be an array
        return np.hstack(weightMatrix)

    def __unflattenWeights(self, flatWeights):
        network = []
        isFirst = True
        lastLayer = []
        currIndex = 0
        for layer in self.config.layers:
            # If its the first layer, the bias is accounted in the input size
            if isFirst:
                weightCount = self.inputSize
                # Modify first flag
                isFirst = False
            # If its another layer, the weights are the number of
            # perceptrons in previous layer + 1 (bias)
            else:
                weightCount = lastLayer[1] + 1
            # layer[0] = activation, layer[1] = perceptron count

            layerWeights = []
            for _ in range(0, layer[1]):
                layerWeights.append(flatWeights[currIndex:currIndex+weightCount])
                currIndex += weightCount
            
            # Append the array of weights of current layer
            network.append(np.array(layerWeights))
            # Store previous layer
            lastLayer = layer
        return np.array(network, dtype=object)

    def __rebuildNetwork(self, flatWeights):
        weightMatrix = self.__unflattenWeights(flatWeights)

        for row in range(0, weightMatrix.shape[0]):
            for col in range(0, self.config.layers[row][1]):
                self.network[row][col].setWeights(weightMatrix[row][col])
        
    def __forwardPropagate(self, input, storeLatent = False, offsetStart = 0, offsetValues = [0,0]):
        """Method to forward propagate an input to obtain a prediction from the network

        Parameters:
            input --> Input point (with bias) to be forwarded

            storeLatent --> Flag to determine if the latent portion is stored or not

            offsetStart --> Index to start the forward propagation from, used mainly in generation from latent code

            offsetValues --> Values to be passed on to the network when offsetting, it is required if offsetStart is used
        Returns:
            summationValues --> np.array of np.array of the different summation values calculated

            activationValues --> np.array of np.array of the different activation values calculated, the last array is the prediction
        """
        activationValues = []
        summationValues = []
        for index, layer in enumerate(self.network):
            # If not in the desired offset start, fill it with empty to avoid index errors
            if index < offsetStart - 1:
                activationValues.append(np.array([]))
                summationValues.append(np.array([]))
            # If in the layer before, fill it with the values
            # Add a [1] to account for the bias not present in the points
            elif index == offsetStart - 1:
                activationValues.append(np.array([1] + offsetValues))
                summationValues.append(np.array(offsetValues))
            # From the layer onwards, operate normally
            else:
                # Get data to pass to layer, use training input or activated data before
                data = input if index == 0 else activationValues[index - 1]
                # Perform all summations
                summationValues.append(
                    np.array([perceptron.summation(data) for perceptron in layer]))
                # Perform all activations
                activations = [layer[i].activate(
                    summationValues[index][i]) for i in range(len(summationValues[index]))]
                # Store the latent code only on the layer with 2 perceptrons
                if storeLatent and layer.shape[0] == 2:
                    self.latentCode.append(activations)
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
        # Add 1 to the input to account for the bias
        initialBackpropagation = [perceptron.initialBackpropagate(
            summations[-1][index], input[index + 1], activations[-1][index]) for index, perceptron in enumerate(self.network[-1])]
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
            # print(expected[i][1:], activ[-1])
            error = error + self.__computeInputError(expected[i][1:], activ[-1])
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

    def generate(self, latentInputs):
        """Method to generate a new datapoint from the latent code

        Parameters:
            latentInputs --> Array of arrays with 2 elements to be fed into the decoder
        Returns:
            results --> Array of values where each value is an array of [latentInput, activationResult]
        """
        # Start index is the index of the latent layer + 1
        startIndex = np.ceil(self.networkSize/2)
        results = []
        for latentInput in latentInputs:
            _, activ = self.__forwardPropagate(input, offsetStart=startIndex, offsetValues=latentInput)
            results.append([latentInput, activ[-1]])
        return results

    def train(self, input, expected):
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
                # Reset latent code
                if self.config.plotLatent:
                    self.latentCode = []
                # Iterate through the dataset order
                for itemIndex in indexes:
                    # Forward propagation
                    summationValues, activationValues = self.__forwardPropagate(
                        input[itemIndex], storeLatent=self.config.plotLatent)
                    # Backpropagation
                    backpropagationValues = self.__backPropagate(
                        input[itemIndex], summationValues, activationValues)
                    # Weight correction
                    self.__correctWeights(
                        input[itemIndex], backpropagationValues, activationValues)
                # Calculate error once epoch is finished
                error = self.__calculateError(input, expected)
                errors.append(error)
                # Increment iterations
                iterations += 1
            # Printing the error
            print(f'Final loss is {errors[-1]}')
            # Plotting the latent code
            if self.config.plotLatent:
                plotLatentSpace(self.latentCode)
        except KeyboardInterrupt:
            print("Finishing up...")


    def cost(self, flatWeights, input, expected):
        self.__rebuildNetwork(flatWeights)
        error = self.__calculateError(input, expected)
        print('ERROR', error)
        return error

    def trainMinimizer(self, input, optimizer):
        # Flatten the weights matrix
        flattenedWeights = self.__flattenNetwork()
        print(flattenedWeights.shape)
        # Minimize the cost function
        res = minimize(fun=self.cost, x0=flattenedWeights, args=(input, input), method=optimizer)
        # res = minimize(fun=self.cost, x0=flattenedWeights, args=(input, input), method=optimizer, options={'maxiter':10})
        # Rebuild the weights matrix
        self.__rebuildNetwork(flattenedWeights)
        # Error of the cost function
        error = res.fun
        print(f'Final loss is {error}')

        return error