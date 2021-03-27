import numpy as np

def getRelativeFitnesses(fitnesses):
    total = np.sum(fitnesses)
    return fitnesses/total

# Calculates minimum fitness and the average fitness
def getFitnessStats(chs):
    # Store the fitness of the characters in an array
    fitnesses = np.array([ch.fitness for ch in chs])
    return np.amin(fitnesses), np.average(fitnesses)