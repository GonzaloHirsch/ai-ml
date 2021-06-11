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

    def __init__(self, inputs, layers, iterations, learningRate, error, beta, alpha, momentum, calculateMetrics, plotLatent, mode, generatorPoints, optimizer, noise):
        if Config.__instance != None:
            raise Exception("Cannot create another instance of config")

        self.input = inputs
        self.iterations = iterations
        self.learningRate = learningRate
        self.beta = beta
        self.error = error
        self.layers = [[layer[ConfigOptions.ACTIVATION.value], layer[ConfigOptions.PERCEPTRONS.value]] for layer in layers]
        self.momentum = momentum
        self.alpha = alpha
        self.plotLatent = plotLatent
        self.mode = mode
        self.generatorPoints = generatorPoints
        self.optimizer = optimizer
        self.noiseCount = noise['count']
        self.noiseProbability = noise['probability']

        Config.__instance = self
    
    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
