# Lib imports
from math import tanh, copysign
import numpy as np
# Local imports
from ActivationOptions from constants

class Perceptron:
    def __init__(self, weightsAmount, activationMethod, learningRate):

        self.weights = np.zeros(weightsAmount) # Size N
        self.activation = activations[activationMethod]
        self.learningRate = learningRate

    def predict(self, inputs):
        summation = self.summation(inputs)        
        return self.activation(summation)

    def correctWeights(self, inputs, desired, prediction): 
        self.weights = self.weights + self.weightCorrectionFactor(inputs, desired, prediction)

    # TODO
    def calculateError(self):
        return

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    def summation(self, inputs):
        # Input shape (1, N)
        # Weight shape (N, 1)
        return np.dot(inputs, self.weights) 
        
    def __simpleActivation(summation):
        # Summation = number
        # Activation = number
        return copysign(1, summation)

    def __linearActivation(summation):
        return

    def __nonLinearActivation(summation):
        return

    def weightCorrectionFactor(self, inputs, desired, prediction):
        # Inpute shape (1, N)
        # Return type (N, 1)
        return self.learningRate * (desired - prediction) * np.transpose(inputs)

    def __str__(self):
        subs = 'weights=%s, learningRate=%s' % (self.weights, self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s

    activations = {
        ActivationOptions.SIMPLE.value: __simpleActivation, 
        ActivationOptions.LINEAR.value: __linearActivation, 
        ActivationOptions.NON_LINEAR.value: __nonLinearActivation
    }
