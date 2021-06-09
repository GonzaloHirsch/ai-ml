# Lib imports
import numpy as np
from math import floor
# Local imports
from perceptron import Perceptron
from helper import printIterationsInPlace, getRandomDatasetOrder
from graphing import plotLatentSpace


class VaeNetwork:
    """Class to represent a Neural Network made of Perceptrons and the methods to train and predict with it
    """

    def __init__(self, config, inputSize):
        # Dimension of the input
        self.inputSize = inputSize
        self.midLayer = floor(len(config.layers) / 2)
        # Create the network
        self.encoder, self.decoder, self.parallelNetwork = self.__createNetwork(
            config, inputSize)
        # Store size to access it only once
        self.encoderSize, self.decoderSize, self.parallelNetworkSize = self.encoder.shape[
            0], self.decoder.shape[0], self.parallelNetwork.shape[0]
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
        encoder, decoder, parallelNetwork, lastLayer = [], [], [], []
        isFirst = True
        layerCount = 0
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
            # The z mean and log variance layers are parallel
            if layerCount == self.midLayer:
                # Both Z MEAN and Z LOG VARIANCE have 2 perceptrons
                # Creating Z MEAN layer, with linear activation
                parallelNetwork.append(np.array([Perceptron(weightCount, 'linear', config.learningRate, config.beta,
                                                            config.momentum, config.alpha) for x in range(0, 2)], dtype=Perceptron))
                # Creating Z LOG VARIANCE layer, with linear activation
                parallelNetwork.append(np.array([Perceptron(weightCount, 'linear', config.learningRate, config.beta,
                                                            config.momentum, config.alpha) for x in range(0, 2)], dtype=Perceptron))
                # Create the middle layer
                # network.append(np.array([Perceptron(weightCount, layer[0], config.learningRate, config.beta,
                #            config.momentum, config.alpha) for x in range(0, layer[1])], dtype=Perceptron))
            elif layerCount > self.midLayer:
                decoder.append(np.array([Perceptron(weightCount, layer[0], config.learningRate, config.beta,
                                                    config.momentum, config.alpha) for x in range(0, layer[1])], dtype=Perceptron))
            else:
                encoder.append(np.array([Perceptron(weightCount, layer[0], config.learningRate, config.beta,
                                                    config.momentum, config.alpha) for x in range(0, layer[1])], dtype=Perceptron))

            # Store previous layer
            lastLayer = layer
            layerCount += 1
        return np.array(encoder, dtype=object), np.array(decoder, dtype=object), np.array(parallelNetwork, dtype=object)

    def __sampling(self, zMean, zLogVariance):
        # Sample from normal distribution with mean 0, stdev 1
        epsilon = np.random.normal(0, 1, (2))
        return zMean + np.exp(zLogVariance / 2) * epsilon, epsilon

    def __activateLayer(self, layer, pastActivations):
        summationValues = np.array(
            [perceptron.summation(pastActivations) for perceptron in layer])
        # Perform all activations
        activationValues = np.array([layer[i].activate(
            summationValues[i]) for i in range(len(summationValues))])
        return summationValues, activationValues

    def __forwardPropagate(self, input):
        """Method to forward propagate an input to obtain a prediction from the network

        Parameters:
            input --> Input point (with bias) to be forwarded
        Returns:
            summationValues --> np.array of np.array of the different summation values calculated

            activationValues --> np.array of np.array of the different activation values calculated, the last array is the prediction
        """
        encoderActivationValues, encoderSummationValues = [], []
        decoderActivationValues, decoderSummationValues = [], []
        # Perform the encoding operations
        for index, layer in enumerate(self.encoder):
            # Get data to pass to layer, use training input or activated data before
            data = input if index == 0 else encoderActivationValues[index - 1]
            # Perform all summations
            encoderSummationValues.append(
                np.array([perceptron.summation(data) for perceptron in layer]))
            # Perform all activations
            activations = [layer[i].activate(
                encoderSummationValues[index][i]) for i in range(len(encoderSummationValues[index]))]
            # If it's not the last layer, add bias to activations for next iterations
            activations = [1] + activations
            encoderActivationValues.append(np.array(activations))

        # Activate zMean and zLogVar layers
        zMeanSumm, zMeanActivation = self.__activateLayer(
            self.parallelNetwork[0], encoderActivationValues[-1])
        zLogVarSumm, zLogVarActivation = self.__activateLayer(
            self.parallelNetwork[1], encoderActivationValues[-1])
        samplingResult, epsilonSample = self.__sampling(
            zMeanActivation, zLogVarActivation)
        # Sample the distribuiton, add a 1 for the bias
        sampledData = np.concatenate((np.array([1]), samplingResult))

        # Perform the decoding operations
        for index, layer in enumerate(self.decoder):
            # Get data to pass to layer, use training input or activated data before
            data = sampledData if index == 0 else decoderActivationValues[index - 1]
            # Perform all summations
            decoderSummationValues.append(
                np.array([perceptron.summation(data) for perceptron in layer]))
            # Perform all activations
            activations = [layer[i].activate(
                decoderSummationValues[index][i]) for i in range(len(decoderSummationValues[index]))]
            # If it's not the last layer, add bias to activations for next iterations
            if index < self.decoderSize - 1:
                activations = [1] + activations
            decoderActivationValues.append(np.array(activations))

        # Perform the sampling
        return encoderSummationValues, encoderActivationValues, decoderSummationValues, decoderActivationValues, zMeanSumm, zMeanActivation, zLogVarSumm, zLogVarActivation, epsilonSample, sampledData

    def __backPropagate(self, input, encSumm, encActiv, decSumm, decActiv, zMeanSumm, zMeanActiv, zLogVarSumm, zLogVarActiv, eSample):
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
            decSumm[-1][index], input[index + 1], decActiv[-1][index]) for index, perceptron in enumerate(self.decoder[-1])]

        # Backpropagate the decoder values
        # Create array of fixed size and set last value
        decBackpropValues = [None] * self.decoderSize
        decBackpropValues[-1] = np.array(initialBackpropagation)
        # Use from size-2 to avoid out of bounds and last layer
        # Use -1 as stop to finish in layer 0 and -1 in step to go in inverse direction
        for index in range(self.decoderSize - 2, -1, -1):
            # Iterate each perceptron in layer
            data = []
            for subindex, perceptron in enumerate(self.decoder[index]):
                # Get all weights leaving that perceptron
                # Add 1 to index to take into account bias
                outboundWeights = np.array(
                    [p.weights[subindex + 1] for p in self.decoder[index + 1]])
                # Calculate backpropagation for next layer in iteration
                data.append(perceptron.backpropagate(
                    decSumm[index][subindex], outboundWeights, decBackpropValues[index + 1]))
            # Add all backpropagation values
            decBackpropValues[index] = np.array(data)

        # Calculate kl loss term
        klLossMean = -0.5 * np.sum(2 * zMeanActiv)
        klLossLogVar = -0.5 * np.sum(1 - np.exp(zLogVarActiv))
        # Calculate backpropagation for middle layers
        parallelBackpropValues = np.append(np.array([perceptron.backpropagate(zMeanSumm, np.array([1] * len(decBackpropValues[0])), decBackpropValues[0]) for perceptron in self.parallelNetwork[0]]) +
                                           klLossMean, np.array([perceptron.backpropagate(zLogVarSumm, np.array([1] * len(decBackpropValues[0])), decBackpropValues[0]) for perceptron in self.parallelNetwork[1]]) + klLossLogVar)

        # Backpropagate the encoder values
        # Create array of fixed size and set last value
        encBackpropValues = [None] * self.encoderSize
        # Use from size-2 to avoid out of bounds and last layer
        # Use -1 as stop to finish in layer 0 and -1 in step to go in inverse direction
        for index in range(self.encoderSize - 1, -1, -1):
            if index == self.encoderSize - 1:
                # Iterate each perceptron in layer
                data = []
                for subindex, perceptron in enumerate(self.encoder[index]):
                    # Get all weights leaving that perceptron
                    # Add 1 to index to take into account bias
                    outboundWeights = np.array(
                        [p.weights[subindex + 1] for p in self.parallelNetwork[0]] + [p.weights[subindex + 1] for p in self.parallelNetwork[1]])
                    # Calculate backpropagation for next layer in iteration
                    data.append(perceptron.backpropagate(
                        encSumm[index][subindex], outboundWeights, parallelBackpropValues))
            else:
                # Iterate each perceptron in layer
                data = []
                for subindex, perceptron in enumerate(self.encoder[index]):
                    # Get all weights leaving that perceptron
                    # Add 1 to index to take into account bias
                    outboundWeights = np.array(
                        [p.weights[subindex + 1] for p in self.encoder[index + 1]])
                    # Calculate backpropagation for next layer in iteration
                    data.append(perceptron.backpropagate(
                        encSumm[index][subindex], outboundWeights, encBackpropValues[index + 1]))
            # Add all backpropagation values
            encBackpropValues[index] = np.array(data)

        return encBackpropValues, parallelBackpropValues, decBackpropValues

    def __correctWeights(self, input, encBackprop, parallelBackprop, decBackprop, encActiv, decActiv, zMeanActiv, zLogVarActiv, sampledData):
        """Method to corrects weights through the network

        Parameters:
            input --> Input point (with bias) to be forwarded

            backpropagations --> Backpropagation values calculated through the backpropagation

            activations --> Activation values calculated through the forward propagation
        Returns:
            Nothing, it updates the values across the network
        """
        # Correct weights
        for index, layer in enumerate(self.encoder):
            # Determine which data using depending on index
            data = input if index == 0 else encActiv[index - 1]
            # Call weight correction on each one
            for subindex, p in enumerate(layer):
                p.correctHiddenWeights(encBackprop[index][subindex], data)

        # Correct weights
        for index, layer in enumerate(self.parallelNetwork):
            # Determine which data using depending on index
            data = encActiv[-1]
            # Call weight correction on each one
            for subindex, p in enumerate(layer):
                p.correctHiddenWeights(parallelBackprop[2 * index + subindex], data)

        # Correct weights
        for index, layer in enumerate(self.decoder):
            # Determine which data using depending on index
            data = sampledData if index == 0 else decActiv[index - 1]
            # Call weight correction on each one
            for subindex, p in enumerate(layer):
                p.correctHiddenWeights(decBackprop[index][subindex], data)

    def __computeInputError(self, actualData, predictedData, zMean, zLogVariance):
        """Method to compute the ||X-X'||^2 distance error

        Parameters:
            actualData --> Expected data

            predictedData --> Predicted data
        Returns:
            Float, error calculated
        """
        print(predictedData)
        xentLoss = -1 * predictedData.shape[0] * \
            np.dot(actualData, np.log(predictedData))
        klLoss = -0.5 * np.sum(1 + zLogVariance -
                               (zMean**2) - np.exp(zLogVariance))
        return np.mean(xentLoss + klLoss)

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
            _, _, _, decActiv, _, zMeanActiv, _, zLogVarActiv, _, _ = self.__forwardPropagate(
                input[i])
            # print(expected[i][1:], activ[-1])
            error = error + \
                self.__computeInputError(
                    expected[i][1:], decActiv[-1], zMeanActiv, zLogVarActiv)
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
            _, activ = self.__forwardPropagate(
                input, offsetStart=startIndex, offsetValues=latentInput)
            results.append([latentInput, activ[-1]])
        return results

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
                # Reset latent code
                # if self.config.plotLatent:
                #     self.latentCode = []
                # Iterate through the dataset order
                for itemIndex in indexes:
                    # Forward propagation
                    encSumm, encActiv, decSumm, decActiv, zMeanSumm, zMeanActiv, zLogVarSumm, zLogVarActiv, eSample, sampledData = self.__forwardPropagate(
                        input[itemIndex])
                    # Backpropagation
                    encBackprop, parallelBackprop, decBackprop = self.__backPropagate(
                        input[itemIndex], encSumm, encActiv, decSumm, decActiv, zMeanSumm, zMeanActiv, zLogVarSumm, zLogVarActiv, eSample)
                    # Weight correction
                    self.__correctWeights(
                        input[itemIndex], encBackprop, parallelBackprop, decBackprop, encActiv, decActiv, zMeanActiv, zLogVarActiv, sampledData)
                # Calculate error once epoch is finished
                error = self.__calculateError(input, input)
                print(error)
                errors.append(error)
                # Increment iterations
                iterations += 1
            # Printing the error
            print(f'Final loss is {errors[-1]}')
            # Plotting the latent code
            # if self.config.plotLatent:
            #     plotLatentSpace(self.latentCode)
        except KeyboardInterrupt:
            print("Finishing up...")
