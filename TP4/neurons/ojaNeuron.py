# Lib imports
from numpy import sqrt, copy, dot
from numpy.random import rand

class OjaNeuron:
    def __init__(self, weightsAmount, learningRate):
        
        self.weights = rand(weightsAmount) * sqrt(1/weightsAmount)
        self.learningRate = learningRate

    def getWeights(self):
        return copy(self.weights)

    def updateLearningRate(self, iteration):
        self.learningRate = 1 / iteration

    # Input shape (1, N)
    # Weight shape (N, 1)
    def summation(self, inputs):
        return dot(inputs, self.weights) 
    
    def correctWeights(self, summation, inputs): 
        delta = self.learningRate * summation * (inputs - (summation * self.weights))
        self.weights += delta

    def __str__(self):
        subs = 'weights=%s, learningRate=%s' % (self.weights, self.learningRate)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    

    
