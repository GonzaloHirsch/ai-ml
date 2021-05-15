# Lib imports
from numpy import array, ndindex

class KohonenNeuron:
    def __init__(self, initialWeight, shape):
        self.completeCounter = 0
        self.lastEpochCounter = 0
        self.countries = []
        self.weights = initialWeight
        self.neighbours = [array([i, j]) for i, j in ndindex(shape)]

    def newDataEntry(self):
        self.completeCounter += 1

    def lastEpochEntry(self, country):
        self.lastEpochCounter += 1
        self.countries.append(country)

    def getWeights(self):
        return self.weights

    def getCompleteCounter(self):
        return self.completeCounter

    def getLastEpochCounter(self):
        return self.lastEpochCounter

    def getCountries(self):
        return self.countries

    def getNeighbours(self):
        return self.neighbours

    def setNeighbours(self, neighbours):
        self.neighbours = neighbours

    def correctWeights(self, learningRate, dataInput): 
        delta = learningRate * (dataInput - self.weights)
        self.weights += delta

    def __str__(self):
        subs = 'weights=%s' % (self.weights)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    

    
