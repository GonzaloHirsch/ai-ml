# Lib imports
from numpy import array, ndindex, zeros, exp
from numpy.linalg import norm
import math
from random import randint
from visualization import plot_kohonen_colormap
from neurons.kohonenNeuron import KohonenNeuron
from helper import writeMatrixToFile
from helper import printIterationsInPlace

# VER SI HAY QUE CAMBIAR LOS PESOS DE LA NEURONA GANADORA
def apply(config, inputs, inputNames):
    try:
        kohonen = Kohonen(config, inputs, inputNames)
        kohonen.learn()
        neuronCounterMatrix = kohonen.getNeuronCounterMatrix(True)
        lastNeuronCounterMatrix = kohonen.getNeuronCounterMatrix(False)
        eucDistMatrix = kohonen.calculateWeightDistanceMatrix()

        # Plotting matrices
        plot_kohonen_colormap(neuronCounterMatrix, k=config.k, filename='colormap-plot.png', addLabels=False)
        plot_kohonen_colormap(lastNeuronCounterMatrix, k=config.k, filename='last-iter-plot.png')
        plot_kohonen_colormap(eucDistMatrix, k=config.k, colormap='Greys', filename='u-matrix-plot.png')
        
        # Print where each country landed on
        kohonen.printLastIterationData()

        # Writing matrices to files
        writeMatrixToFile(('counterMatrix_%s.txt' % (config.k)), neuronCounterMatrix)
        writeMatrixToFile(('lastCounterMatrix_%s.txt' % (config.k)), lastNeuronCounterMatrix)
        writeMatrixToFile(('eucDistMatrix_%s.txt' % (config.k)), eucDistMatrix)

    except KeyboardInterrupt:
        print("Finishing up...")

class Kohonen:
    def __init__(self, config, inputs, inputNames):
        
        self.inputs = inputs
        self.inputNames = inputNames
        self.k = config.k
        self.iterations = config.iterations
        self.network = self.createKohonenNetwork()

    def createKohonenNetwork(self):
        network = []

        for _ in range(0, self.k):
            network.append(
                array(
                    [KohonenNeuron(self.inputs[randint(0, self.inputs.shape[0]-1)], (self.k, self.k)) for _ in range(0, self.k)], 
                    dtype = KohonenNeuron
                )
            )

        return array(network, dtype = object)

    def getWinningNeuron(self, inputData, country = ''): 
        minDist = 214748364
        row = 0
        col = 0

        for i, j in ndindex(self.network.shape):
            neuron = self.network[i][j]
            # Euclidean distance between data and weight
            dist = norm(neuron.getWeights()-inputData)
   
            # winning neuron is the one with minimum distance
            if dist <= minDist:
                minDist = dist
                row = i
                col = j                

        # Add 1 to the amount of data that landed on the winning neuron
        self.network[row][col].newDataEntry()
        # If it is the last iteration, countries which passed through the winning neuron are stored
        if country != '':
            self.network[row][col].lastEpochEntry(country)
        
        return row, col

    # Want the positions of the neurons that live within a certain radius
    # of the neuron I'm analyzing
    def getNeuronNeighbours(self, row, col, radius): 
        neuronPos = array([row, col])
        neuron = self.network[row][col]
        currNeighbours = neuron.getNeighbours()
        newNeighbours = []

        for currPos in currNeighbours:
            # Euc distance in the matrix positions
            dist = norm(neuronPos - currPos)
            # Will be considered a neighbour if it is inside the radius
            if dist <= radius:
                newNeighbours.append(currPos)

        neuron.setNeighbours(newNeighbours)

        return newNeighbours

    def calculatePositionDistance(self, firstPos, secondPos):
        return norm(firstPos-secondPos)

    # Updating the weights of the neighbouring neurons
    def updateNeuronsWeights(self, neurons, learningRates, inputData):
        for i in range(0, len(neurons)):
            # Neuron whose weights will be updated
            neuron = self.network[neurons[i][0]][neurons[i][1]]
            # Updates of weights
            neuron.correctWeights(learningRates[i], inputData)

    def getRadius(self, t):
        lmt = self.k * math.sqrt(2)
        return ((1-lmt)/self.iterations) * t + lmt

    def getLearningRate(self, iteration):
        return 1/(self.iterations * 0.25) if iteration <= (self.iterations * 0.25) else 1/iteration

    def getLearningRateForNeighbours(self, learningRate, radius, neuron, neighbours):
        distance = array([norm(neuron - neighbour) for neighbour in neighbours])
        return exp(-1 * distance / radius) * learningRate

    def getNeuronCounterMatrix(self, isComplete):
        neuronCounterMatrix = zeros(shape=(self.k, self.k))

        for i, j in ndindex(self.network.shape):

            if isComplete:
                # Matrix with the count of all the data that went through each neuron
                neuronCounterMatrix[i][j] = self.network[i][j].getCompleteCounter()
            else:
                # Matrix with data that went through the neuron on the last iteration
                neuronCounterMatrix[i][j] = self.network[i][j].getLastEpochCounter()

        return neuronCounterMatrix

    def calculateWeightDistanceMatrix(self):
        eucDistMatrix = zeros(shape=(self.k, self.k))
        # Weight will be 1 in the last iteration
        radius = 1

        for i, j in ndindex(self.network.shape):
            neighbours = self.getNeuronNeighbours(i, j, radius)
            eucDistMatrix[i][j] = self.calculateAverageEucDist(self.network[i][j], neighbours)

        return eucDistMatrix


    def calculateAverageEucDist(self, neuron, neighbours):
        average = 0

        for i in range(0, len(neighbours)):
            row = neighbours[i][0]
            col = neighbours[i][1]
            neighbor = self.network[row][col]

            dist = norm(neuron.getWeights()-neighbor.getWeights())
            average += dist

        average /= len(neighbours)

        return average

    
    def learn(self):
        iteration = 0
        inputsCount = self.inputs.shape[0]

        for iteration in range(0, self.iterations):
            # Will determine what type of data should be stored
            lastIter = True if iteration == self.iterations-1 else False
            # Learning rate for the iteration
            learningRate = self.getLearningRate(iteration)
            # Get the radius for vecinity
            radius = self.getRadius(iteration)

            printIterationsInPlace(iteration)

            for inputIdx in range(0, inputsCount):
                # Input data of the contry being analyzed
                inputData = self.inputs[inputIdx]
                # Row and column of the winning neuron
                row, col = self.getWinningNeuron(inputData, self.inputNames[inputIdx] if lastIter else '')
                # Neighbours = neurons within a certain radius of the winning neuron
                neighbours = self.getNeuronNeighbours(row, col, radius)
                # Array of modified learning rates for the neighbours
                learningRates = self.getLearningRateForNeighbours(learningRate, radius, array([row, col]), neighbours)
                # Updating the weights of the neighbour neurons
                self.updateNeuronsWeights(neighbours, learningRates, inputData)

    def printLastIterationData(self):
        print("---------------------\nPos\tCountries")
        for i, j in ndindex(self.network.shape):
            print(('[%i, %i]\t%s' % (i, j, self.network[i][j].getCountries())))
