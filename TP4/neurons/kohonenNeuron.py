# Lib imports
from numpy import sqrt, copy, dot
from numpy.random import rand
import random

class KohonenNeuron:
    def __init__(self, weightsAmount):
        self.dataCounter = 0
        self.weights = rand(weightsAmount) * sqrt(1/weightsAmount)

    def newDataEntry(self):
        self.dataCounter += 1

    def getWeights(self):
        return copy(self.weights)

    def getCounter(self):
        return self.dataCounter

    def correctWeights(self, learningRate, dataInput): 
        delta = learningRate * (dataInput - self.weights)
        self.weights += delta

    def __str__(self):
        subs = 'weights=%s' % (self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    

    
