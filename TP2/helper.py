import numpy as np

def getRelativeFitnesses(fitnesses):
    total = np.sum(fitnesses)
    return fitnesses/total

# Calculates minimum fitness and the average fitness
def getFitnessStats(chs):
    fitnesses = np.array([])
    # Store the fitness of the characters in an array
    for ch in chs:
        fitnesses = np.append(fitnesses, ch.fitness)
    return np.amin(fitnesses), np.average(fitnesses)