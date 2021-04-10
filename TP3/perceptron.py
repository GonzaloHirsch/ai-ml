# Lib imports
from math import tanh
import numpy as np
# Local imports
from ActivationOptions from constants

class Perceptron:
    def __init__(self, weightsAmount, activationMethod):

        self.weights = np.zeros(weightsAmount)
        self.activation = activations[activationMethod]

    def __simpleActivation():
        return

    def __linearActivation():
        return

    def __nonLinearActivation():
        return

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    # def __str__(self):
    #     subs = 'fitness=%s => arma=%s, botas=%s, casco=%s, guantes=%s, pechera=%s, height=%s' % (self.fitness, self.rawGenes[0][1], self.rawGenes[1][1], self.rawGenes[2][1], self.rawGenes[3][1], self.rawGenes[4][1], self.rawGenes[5])
    #     s = '%s{%s}' % (type(self).__name__, subs)
    #     return s
    
    # def __computeHashString(self):
    #     return hash((self.rawGenes[0][1], self.rawGenes[1][1], self.rawGenes[2][1], self.rawGenes[3][1], self.rawGenes[4][1], round(self.rawGenes[5], 2)))
        
    # def __hash__(self):
    #     if self.computedHash == None:
    #         self.computedHash = self.__computeHashString()
    #     return self.computedHash

    activations = {
        ActivationOptions.SIMPLE.value: __simpleActivation, 
        ActivationOptions.LINEAR.value: __linearActivation, 
        ActivationOptions.NON_LINEAR.value: __nonLinearActivation
    }
