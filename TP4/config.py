# Local Imports
from constants import ConfigOptions

class Config:
    __instance = None

    # Asumes the class was instantiated once
    @staticmethod
    def getInstance():
        if Config.__instance == None:
            raise Exception("No config instance available")
        return Config.__instance

    def __init__(self, input, test, flatten, iterations, learningRate, network, k):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.input = input
        self.test = test
        self.flatten = flatten
        self.iterations = iterations
        self.learningRate = learningRate
        self.network = network
        self.k = k

        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
