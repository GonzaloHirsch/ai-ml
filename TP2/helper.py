import numpy as np

def getRelativeFitnesses(fitnesses):
    total = np.sum(fitnesses)
    return fitnesses/total