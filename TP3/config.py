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

    def __init__(self, inputs, flatten, desired, iterations, activation, learningRate, multilayer, error, layers, normalizeDesired, beta, delta, alpha, momentum, blockAmount, testBlock):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.input = inputs
        self.flatten = flatten
        self.desired = desired
        self.iterations = iterations
        self.activation = activation
        self.learningRate = learningRate
        self.beta = beta
        self.multilayer = multilayer
        self.error = error
        self.layers = [[layer[ConfigOptions.ACTIVATION.value], layer[ConfigOptions.PERCEPTRONS.value]] for layer in layers]
        self.normalizeDesired = normalizeDesired
        self.delta = delta
        self.momentum = momentum
        self.alpha = alpha
        self.blockAmount = blockAmount
        self.testBlock = testBlock

        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
