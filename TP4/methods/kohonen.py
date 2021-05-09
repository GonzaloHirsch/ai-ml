import numpy as np
import math
import random 

from neurons.kohonenNeuron import KohonenNeuron

# TODO FALTA NORMALIZAR LOS VECTORES!!
def apply(config, inputs):
    try:
        kohonen = Kohonen(config, inputs)
        kohonen.learn()
    except KeyboardInterrupt:
        print("Finishing up...")

class Kohonen:
    def __init__(self, config, inputs):
        
        self.inputs = inputs
        self.k = config.k
        self.iterations = config.iterations
        self.network = self.createKohonenNetwork()

    def createKohonenNetwork(self):
        network = []

        for i in range(0, self.k):
            network.append(np.array([KohonenNeuron(int(self.inputs.shape[1])) for x in range(0, self.k)], dtype = KohonenNeuron))

        return np.array(network, dtype = object)

    def getWinningNeuron(self, inputData): 
        minDist = None
        row = 0
        col = 0

        for i in range(0, self.k):
            for j in range(0, self.k):
                neuron = self.network[i][j]
                # Euclidean distance between data and weight
                dist = np.linalg.norm(neuron.getWeights()-inputData)
   
                if minDist is None:
                    minDist = dist

                # winning neuron is the one with minimum distance
                elif dist <= minDist:
                    minDist = dist
                    row = i
                    col = j

        return row, col

    # Want the positions of the neurons that live within a certain radius
    # of the neuron I'm analyzing
    def getNeuronNeighbours(self, row, col, radius): 
        neuronPos = np.array([row, col])
        neighbours = []

        for i in range(0, self.k):
            for j in range(0, self.k):
                currPos = np.array([i, j])
                dist = np.linalg.norm(neuronPos-currPos)

                if dist <= radius:
                    neighbours.append(currPos)

        return neighbours

    # Updating the weights of the neighbouring neurons
    def updateNeuronsWeights(self, neurons, learningRate, inputData):
        # print("LEARNING RATE = ", learningRate)
        # print("INPUT = ", inputData)
        for i in range(0, len(neurons)):
            row = neurons[i][0]
            col = neurons[i][1]
            neuron = self.network[row][col]
            # print("BEFORE = ", neuron.getWeights())
            neuron.correctWeights(learningRate, inputData)
            # print("AFTER = ", neuron.getWeights())

    def getRadius(self, t):
        return ((1 - 2 * math.sqrt(self.k)) / (self.iterations)) * (t+1) + 2 * math.sqrt(self.k)

    def getLearningRate(self, iteration):
        if iteration == 0 or iteration == 1:
            return random.uniform(0, 1)

        return 1 / iteration

    
    def learn(self):
        iteration = 0

        for iteration in range(0,self.iterations):

            print("ITERATION = ", iteration)

            learningRate = self.getLearningRate(iteration)

            for inputIdx in range(0, self.inputs.shape[0]):

                inputData = self.inputs[inputIdx]

                row, col = self.getWinningNeuron(inputData)

                radius = self.getRadius(iteration)

                neighbours = self.getNeuronNeighbours(row, col, radius)

                self.updateNeuronsWeights(neighbours, learningRate, inputData)
