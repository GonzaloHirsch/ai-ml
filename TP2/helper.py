from numpy import sum, amin, array, average, unique

def getRelativeFitnesses(fitnesses):
    total = sum(fitnesses)
    return fitnesses/total

# Calculates minimum fitness and the average fitness
def getFitnessStats(chs):
    # Store the fitness of the characters in an array
    fitnesses = array([ch.fitness for ch in chs])
    return amin(fitnesses), average(fitnesses)

# Calculate different combinations present
def getDiversityStats(chs):
    hashes = array([hash(ch) for ch in chs])
    # Count instances of each one
    _, counts = unique(hashes, return_counts=True)
    return len(counts)

# Gets the best character
def getBestCharacter(chs):
    max = 0
    maxCh = None
    for ch in chs:
        if (ch.fitness > max):
            max = ch.fitness
            maxCh = ch
    return maxCh