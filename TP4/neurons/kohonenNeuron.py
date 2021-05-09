# Lib imports
from numpy import sqrt, copy, dot
from numpy.random import rand
import random

class KohonenNeuron:
    def __init__(self, weightsAmount):
        
        self.weights = rand(weightsAmount) * sqrt(1/weightsAmount)

    def getWeights(self):
        return copy(self.weights)

    def correctWeights(self, learningRate, dataInput): 
        delta = learningRate * (dataInput - self.weights)
        self.weights += delta

    def __str__(self):
        subs = 'weights=%s' % (self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    

    
