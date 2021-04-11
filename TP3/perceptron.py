# Lib imports
from math import tanh, copysign
import numpy as np
# Local imports
from ActivationOptions from constants

class Perceptron:
    def __init__(self, weightsAmount, activationMethod, learningRate):

        self.weights = np.zeros(weightsAmount) # Size N
        self.activation = activations[activationMethod]
        self.derivative = derivatives[activationMethod]
        self.learningRate = learningRate

    def summation(self, inputs):
        # Input shape (1, N)
        # Weight shape (N, 1)
        return np.dot(inputs, self.weights) 
    
    def activate(self, summation):
        return self.activation(summation)

    def weightCorrectionFactor(self, inputs, desired, prediction, summation):
        # Inpute shape (1, N)
        # Return type (N, 1)
        dActivation = self.derivative(summation)
        return self.learningRate * (desired - prediction) * dActivation * np.transpose(inputs)

    def correctWeights(self, inputs, desired, summation): 
        self.weights += self.weightCorrectionFactor(inputs, desired, summation)

    # TODO
    def calculateError(self):
        return

    # -----------------------------------------------------------------
    # ACTIVATION FUNCTIONS
    # -----------------------------------------------------------------
        
    def __simpleActivation(summation):
        # Summation = number
        # Activation = number
        return copysign(1, summation)

    # Derivative
    def __dSimpleActivation(summation):
        return 1

    def __linearActivation(summation):
        return

    # Derivative
    def __dLinearActivation(summation):
        return

    def __nonLinearActivation(summation):
        return

    # Derivative
    def __dNonLinearActivation(summation):
        return

    def __str__(self):
        subs = 'weights=%s, learningRate=%s' % (self.weights, self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s

    activations = {
        ActivationOptions.SIMPLE.value: __simpleActivation, 
        ActivationOptions.LINEAR.value: __linearActivation, 
        ActivationOptions.NON_LINEAR.value: __nonLinearActivation
    }

    derivatives = {
        ActivationOptions.SIMPLE.value: __dSimpleActivation, 
        ActivationOptions.LINEAR.value: __dLinearActivation, 
        ActivationOptions.NON_LINEAR.value: __dNonLinearCorrection
    }
