# Lib imports
import numpy as np
from math import floor
from tensorflow import keras
import tensorflow as tf
from scipy import optimize
# Local imports
from perceptron import Perceptron
from helper import printIterationsInPlace, getRandomDatasetOrder, adam
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
                parallelNetwork.append(np.array([Perceptron(weightCount, 'nonlinear', config.learningRate, config.beta,
                                                            config.momentum, config.alpha) for x in range(0, 2)], dtype=Perceptron))
                # Creating Z LOG VARIANCE layer, with linear activation
                parallelNetwork.append(np.array([Perceptron(weightCount, 'nonlinear', config.learningRate, config.beta,
                                                            config.momentum, config.alpha) for x in range(0, 2)], dtype=Perceptron))
                # Create the middle layer in the decoder as the input
                # decoder.append(np.array([Perceptron(3, layer[0], config.learningRate, config.beta,
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
        # return zMean + zLogVariance * epsilon, epsilon

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
        print(zMeanActivation, zLogVarActivation)
        samplingResult, epsilonSample = self.__sampling(
            zMeanActivation, zLogVarActivation)
        # Sample the distribuiton, add a 1 for the bias
        sampledData = np.concatenate((np.array([1]), samplingResult))
        # sampledData = samplingResult

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

    def predict(self, input):
        """Method to calculate a prediction given the input

        Parameters:
            input --> Value to predict from
        Returns:
            np.array with the predicted value
        """
        _, _, _, decActiv, _, zMeanActiv, _, zLogVarActiv, _, _ = self.__forwardPropagate(input)
        return decActiv[-1]

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

    def __computeInputError(self, actualData, predictedData, zMean, zLogVariance):
        """Method to compute the ||X-X'||^2 distance error

        Parameters:
            actualData --> Expected data

            predictedData --> Predicted data
        Returns:
            Float, error calculated
        """
        # print(predictedData)
        # xentLoss = -1 * predictedData.shape[0] * \
        #     np.dot(actualData, np.log(predictedData))
        # klLoss = -0.5 * np.sum(1 + zLogVariance -
        #                        (zMean**2) - np.exp(zLogVariance))
        # return np.mean(xentLoss + klLoss)

        # Aca se computa la cross entropy entre los "labels" x que son los valores 0/1 de los pixeles, y lo que salió al final del Decoder.
        actualData = tf.convert_to_tensor(actualData, dtype=tf.float32)
        predictedData = tf.convert_to_tensor(predictedData, dtype=tf.float32)
        zMean = tf.convert_to_tensor(zMean, dtype=tf.float32)
        zLogVariance = tf.convert_to_tensor(zLogVariance, dtype=tf.float32)
        xent_loss = (predictedData.shape[0]) * keras.metrics.binary_crossentropy(actualData, predictedData) # x-^X
        kl_loss = - 0.5 * keras.backend.sum(1 + zLogVariance - keras.backend.square(zMean) - keras.backend.exp(zLogVariance), axis=-1)
        vae_loss = keras.backend.mean(xent_loss + kl_loss)
        # print(xent_loss, kl_loss)
        return vae_loss

    def __flattenNetwork(self):
        weightMatrix = []
        # Matrix with all the weights as rows
        for layer in self.encoder:
            for perceptron in layer:
                weightMatrix.append(perceptron.getWeights()) 
        for layer in self.parallelNetwork:
            for perceptron in layer:
                weightMatrix.append(perceptron.getWeights()) 
        for layer in self.decoder:
            for perceptron in layer:
                weightMatrix.append(perceptron.getWeights()) 
        
        weightMatrix = np.array(weightMatrix, dtype=object)
        # Flatten the weights matrix to be an array
        return np.hstack(weightMatrix)

    def __rebuildNetwork(self, flatWeights):
        wIndex = 0
        for layer in self.encoder:
            for perceptron in layer:
                perceptron.setWeights(flatWeights[wIndex:wIndex+perceptron.weightsAmount])
                wIndex += perceptron.weightsAmount
        for layer in self.parallelNetwork:
            for perceptron in layer:
                perceptron.setWeights(flatWeights[wIndex:wIndex+perceptron.weightsAmount])
                wIndex += perceptron.weightsAmount
        for layer in self.decoder:
            for perceptron in layer:
                perceptron.setWeights(flatWeights[wIndex:wIndex+perceptron.weightsAmount])
                wIndex += perceptron.weightsAmount

    def __loss(self, weights, input, expected):
        self.__rebuildNetwork(weights)
        # print(weights)
        error = 0
        for i in range(len(input)):
            # Propagate to get the last activation value
            _, _, _, decActiv, _, zMeanActiv, _, zLogVarActiv, _, _ = self.__forwardPropagate(
                input[i])
            # print(expected[i][1:], decActiv[-1])
            _error = self.__computeInputError(expected[i][1:], decActiv[-1], zMeanActiv, zLogVarActiv).numpy()
            error = error + _error
        print(error)
        return error

    def trainMinimizer(self, input, optimizer):
        flattenedWeights = self.__flattenNetwork()
        print(flattenedWeights.shape)
        # Minimize the cost function
        res = optimize.basinhopping(func=self.__loss, x0=flattenedWeights, disp=True, minimizer_kwargs={"args":(input, input), "method": "L-BFGS-B", "options": {"disp": True}})
        # res = adam(fun=self.__loss, x0=flattenedWeights, args=(input, input))
        # Rebuild the weights matrix
        self.__rebuildNetwork(flattenedWeights)
        # Error of the cost function
        error = res.fun
        print(f'Final loss is {error}')
