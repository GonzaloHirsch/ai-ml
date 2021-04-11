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

    def __init__(self, inputs, desired, iterations, activation, learningRate, multilayer):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.input = inputs
        self.desired = desired
        self.iterations = iterations
        self.activation = activation
        self.learningRate = learningRate
        self.multilayer = multilayer

        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
