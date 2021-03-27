from numpy import sum, amin, array, average

def getRelativeFitnesses(fitnesses):
    total = sum(fitnesses)
    return fitnesses/total

# Calculates minimum fitness and the average fitness
def getFitnessStats(chs):
    # Store the fitness of the characters in an array
    fitnesses = array([ch.fitness for ch in chs])
    return amin(fitnesses), average(fitnesses)