# Lib imports
from math import tanh, copysign
import numpy as np
# Local imports
from constants import ActivationOptions 

class Perceptron:
    def __init__(self, weightsAmount, activationMethod, learningRate, beta, momentum, alpha):
        
        self.beta = beta
        self.alpha = alpha
        self.activationMethod = activationMethod
        self.weights = np.random.rand(weightsAmount) * np.sqrt(1/weightsAmount)
        self.weightsAmount = weightsAmount
        self.activation = self.getActivationFunction(activationMethod)
        self.derivative = self.getDerivativeFunction(activationMethod)
        self.learningRate = learningRate
        self.previousCorrection = np.zeros(weightsAmount)
        self.useMomentum = momentum

    def getWeights(self):
        return np.copy(self.weights)

    def setWeights(self, weights):
        self.weights = weights

    def summation(self, inputs):
        # Input shape (1, N)
        # Weight shape (N, 1)
        return np.dot(inputs, self.weights) 
    
    def activate(self, summation):
        return self.activation(summation)

    def backpropagate(self, summation, otherWeights, backpropagations):
        return self.derivative(summation) * np.dot(otherWeights, backpropagations) 

    def initialBackpropagate(self, summation, desired, prediction):
        return self.derivative(summation) * (desired - prediction)

    def initialBackpropagateWithError(self, summation, error):
        return self.derivative(summation) * error

    def correctHiddenWeights(self, backpropagation, prediction):
        correction = self.learningRate * backpropagation * prediction
        # Add correction used in momentum
        if self.useMomentum:
            correction = correction + self.alpha * self.previousCorrection
            self.previousCorrection = correction

        # Updates weights and update the previousWeights
        self.weights = self.weights + correction

    # -----------------------------------------------------------------
    # ERROR FUNCTIONS
    # -----------------------------------------------------------------

    def calculateError(self, desired, prediction):
        return ((desired - prediction)**2) * 0.5

    # -----------------------------------------------------------------
    # ACTIVATION FUNCTIONS
    # -----------------------------------------------------------------
        
    def __simpleActivation(self, summation):
        # Summation = number
        # Activation = number
        return copysign(1, summation)

    # Derivative
    def __dSimpleActivation(self, summation):
        return 1

    def __linearActivation(self, summation):
        return summation

    # Derivative
    def __dLinearActivation(self, summation):
        return 1

    def __nonLinearActivation(self, summation):
        return tanh(self.beta * summation)

    # Derivative
    def __dNonLinearActivation(self, summation):
        return self.beta * (1 - (self.__nonLinearActivation(summation)**2))

    def __reluActivation(self, summation):
        return max(0, summation)

    # Derivative
    def __dReluActivation(self, summation):
        return 0 if summation <= 0 else 1

    def __str__(self):
        subs = 'activation=%s, weights=%s, learningRate=%s' % (self.activationMethod, self.weights, self.learningRate)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s

    def getActivationFunction(self, activationMethod):
        activations = {
            ActivationOptions.SIMPLE.value: self.__simpleActivation, 
            ActivationOptions.LINEAR.value: self.__linearActivation, 
            ActivationOptions.NON_LINEAR.value: self.__nonLinearActivation,
            ActivationOptions.RELU.value: self.__reluActivation
        }
        return activations[activationMethod]

    def getDerivativeFunction(self, activationMethod):
        derivatives = {
            ActivationOptions.SIMPLE.value: self.__dSimpleActivation, 
            ActivationOptions.LINEAR.value: self.__dLinearActivation, 
            ActivationOptions.NON_LINEAR.value: self.__dNonLinearActivation,
            ActivationOptions.RELU.value: self.__dReluActivation
        }
        return derivatives[activationMethod]

    

    
