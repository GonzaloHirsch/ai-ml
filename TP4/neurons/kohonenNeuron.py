# Lib imports
from numpy import sqrt, copy, dot
from numpy.random import rand
import random

class KohonenNeuron:
    def __init__(self, weightsAmount):
        self.completeCounter = 0
        self.lastEpochCounter = 0
        self.countries = []
        self.weights = rand(weightsAmount) * sqrt(1/weightsAmount)

    def newDataEntry(self):
        self.completeCounter += 1

    def lastEpochEntry(self, country):
        self.lastEpochCounter += 1
        self.countries.append(country)

    def getWeights(self):
        return copy(self.weights)

    def getCompleteCounter(self):
        return self.completeCounter

    def getLastEpochCounter(self):
        return self.lastEpochCounter

    def getCountries(self):
        return self.countries

    def correctWeights(self, learningRate, dataInput): 
        delta = learningRate * (dataInput - self.weights)
        self.weights += delta

    def __str__(self):
        subs = 'weights=%s' % (self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    

    
