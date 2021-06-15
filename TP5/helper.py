from random import sample, uniform
from sys import stdout
import numpy as np
from scipy.optimize import OptimizeResult
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = 'output/'

# Returns a random dataset index order based on the dataset length
# Input: number of rows or items in dataset
# Returs: array of mixed indexes
def getRandomDatasetOrder(datasetLength):
    return sample(range(0, datasetLength), datasetLength)

# Prints the iterations in place, creating an iteration counter
# Input: curent iteration number
def printIterationsInPlace(iterations):
    stdout.write("Epoch #{}\r".format(iterations))
    stdout.flush()

# Writes matrix to file 
# Input: file where to write, matrix to write
def writeMatrixToFile(filename, _matrix):
    mat = np.matrix(_matrix)
    with open(OUTPUT_DIR + filename,'wb') as f:
        for line in mat:
            np.savetxt(f, line, fmt='%.2f')

# Creates a directory if the directory doesn't exist
def createDirectoryIfNotExist(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

# creates noise on input based on probability p ( 0 <= p <= 1)
def createNoise(input, p):
    noiseInput = input.copy()

    # First one is the bias and should not be changed
    for idx in range(1, len(input)):
        rnd = uniform(0, 1)

        # If less than probability, alter input
        if rnd <= p:
            if input[idx] == 1:
                noiseInput[idx] = 0
            else:
                noiseInput[idx] = 1
            
    return noiseInput

def adam(
    fun,
    x0,
    jac,
    args=(),
    learning_rate=0.001,
    beta1=0.9,
    beta2=0.999,
    eps=1e-8,
    startiter=0,
    maxiter=1000,
    callback=None,
    **kwargs
):
    """``scipy.optimize.minimize`` compatible implementation of ADAM -
    [http://arxiv.org/pdf/1412.6980.pdf].
    Adapted from ``autograd/misc/optimizers.py``.
    """
    x = x0
    m = np.zeros_like(x)
    v = np.zeros_like(x)

    for i in range(startiter, startiter + maxiter):
        g = jac(x)

        if callback and callback(x):
            break

        m = (1 - beta1) * g + beta1 * m  # first  moment estimate.
        v = (1 - beta2) * (g**2) + beta2 * v  # second moment estimate.
        mhat = m / (1 - beta1**(i + 1))  # bias correction.
        vhat = v / (1 - beta2**(i + 1))
        x = x - learning_rate * mhat / (np.sqrt(vhat) + eps)

    i += 1
    return OptimizeResult(x=x, fun=fun(x), jac=g, nit=i, nfev=i, success=True)


def predictAndPrintResults(network, inputs, expected):
    for i in range(0, len(inputs)):
        print('Original Input:')
        print(expected[i][1:].reshape((7, 5)))
        print('Noise Input')
        print(inputs[i][1:].reshape((7, 5)))
        # Predict with the trained network
        result = network.predict(inputs[i])
        print('Result:')
        print(np.array([0 if e < 0.5 else 1 for e in result]).reshape((7, 5)))

def printCharacter(matrix):
    # Parse input images
    dimensions = (7, 5)
    figure = np.zeros((dimensions[0], dimensions[1]))

    for i in range(0, 7):
        for j in range (0, 5):
            matrix[i][j] = 1 if matrix[i][j] == 0 else 0
    
    figure = matrix
            
    plt.figure(figsize=(7, 7))
    plt.imshow(figure, cmap='Greys_r')
    plt.show()

def concatenateArrays(a1, a2):
    result = []
    for x in a1:
        result.append(x)
    for y in a2:
        result.append(y)

    return np.array(result)