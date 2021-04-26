import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import argparse

EJ1_XOR = "xor1"
EJ1_AND = "and1"
EJ2 = "ej2"
EJ3 = "ej3"

x = np.linspace(-2,2,100)

x2 = np.linspace(-5,5,100)
y2 = np.linspace(-5,5,100)

def calculateR2Hiperplanes(filename):
    f = open(filename, 'r')

    iterativeHiperplanes = []
    index = 0
    for line in f:
        weights = line.lstrip("[").rstrip("]\n\r").split()
        if index > 0:
            if len(weights) != 3:
                print("Can only graph in 2D")
                exit(1)
            else:
                # Creating the y = mx + b function
                # Comes as a + by + cx = 0
                a = float(weights[0])
                c = float(weights[1])
                b = float(weights[2])
                if c != 0:
                    y = (c/(-1*b))*x + (a/(-1*b))
                else:
                    y = 0*x
                iterativeHiperplanes.append(y)

        index += 1

    f.close()

    return iterativeHiperplanes

def calculateR3Hiperplanes(filename):
    f = open(filename, 'r')

    iterativeHiperplanes = []
    index = 0
    for line in f:
        weights = line.lstrip("[").rstrip("]\n\r").split()
        if index > 0:
            if len(weights) != 4:
                print("Can only graph in 3D")
                exit(1)
            else:
                # Comes as a + bz + cy + dx = 0 -> despejo Z
                a = float(weights[0])
                d = float(weights[1])
                c = float(weights[2])
                b = float(weights[3])
                if d != 0:
                    X, Y = np.meshgrid(x2, y2)
                    Z = (a/(-1*b)) + (c/(-1*b))*Y + (d/(-1*b))*X
                else:
                    Z = 0
                iterativeHiperplanes.append(Z)

        index += 1

    f.close()

    return iterativeHiperplanes


def getInputFromFile(inputFile):
    with open(inputFile) as f:
        # Read all lines
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(np.array([float(elem) for elem in line.strip().split()]))
    return np.array(data)

def getErrorInputFromFile(errorFile):
    with open(errorFile) as f:
        # Read all lines
        lines = f.readlines()
        iterations = []
        errors = []
        index = 0
        for line in lines:
            # Skip headers
            if index > 0:
                data = line.rstrip("\n").split(",")
                iterations.append(int(data[0]))
                errors.append(float(data[1]))
            index += 1
    return iterations, errors

def getAccuracyInputFromFile(errorFile):
    with open(errorFile) as f:
        # Read all lines
        lines = f.readlines()
        iterations = []
        accuracies = []
        index = 0
        for line in lines:
            # Skip headers
            if index > 0:
                data = line.rstrip("\n").split(",")
                iterations.append(int(data[0]))
                accuracies.append(float(data[1]))
            index += 1
    return iterations, accuracies


def graphR2Hiperplane(inputs, desired, hiperplanes):
    fig, ax = plt.subplots()

    for i in range(inputs.shape[0]):
        color = [0, 0, 1] if desired[i] > 0 else [1, 0, 0]
        ax.plot(inputs[i][0], inputs[i][1], 'o', c=color)
   
    ax.set_xlabel('x', color='#1C2833')
    ax.set_ylabel('y', color='#1C2833')
    ax.grid()

    ax.set_aspect('equal')
    ax.grid(True, which='both')

    # set the x-spine (see below for more info on `set_position`)
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()


    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()

    plt.xticks(np.arange(-1, 1.1, 0.5))
    plt.yticks(np.arange(-1, 1.1, 0.5))
    plt.xlim(-1.1,1.1)
    plt.ylim(-1.1,1.1)

    line, = ax.plot(x, hiperplanes[0], '-r', label='Iteration 0')

    def animate(i):
        if (i < len(hiperplanes)):
            line.set_ydata(hiperplanes[i])  # update the data.
        return line,

    ani = animation.FuncAnimation(
        fig, animate, interval=200, blit=False, save_count=50)

    plt.show()


def graphR3Hiperplane(inputs, desired, hiperplanes):

    plot_args = {'rstride': 1, 'cstride': 1, 
             'linewidth': 0.01, 'antialiased': True, 'color': [1,0,0],
             'shade': True, 'rstride': 10, 'cstride': 10, 'alpha': 0.75}

    X, Y = np.meshgrid(x2, y2)
    Z = hiperplanes[0]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_zlim(-5, 5)
    ax.set_zlim(-5,5)
    ax.set_zlim(-5,5)
    
    maxd = desired.max()
    for i in range(inputs.shape[0]):
        color = [1, desired[i][0]/maxd, 0.5]
        ax.plot(inputs[i][0], inputs[i][1], inputs[i][2], 'o', c=color)
   
    ax.grid()

    plot = [ax.plot_surface(X, Y, Z, **plot_args)]

    def animate(i, hiperplanes, plot):
        if (i < len(hiperplanes)):
            plot[0].remove()
            plot[0] = ax.plot_surface(X, Y, hiperplanes[i], **plot_args)
        return plot,

    ani = animation.FuncAnimation(
        fig, animate, interval=200, blit=False, fargs=(hiperplanes, plot), save_count=50)

    plt.show()

def graphError(iterations, errors):
    fig, ax = plt.subplots()

    ax.set_xlabel('Iterations', color='#1C2833')
    ax.set_ylabel('Error', color='#1C2833')
    ax.grid()

    ax.plot(iterations, errors, '-b')

    plt.show()


def graphAccuracyComparison(iterations, trainAccuracy, testAccuracy):
    fig, ax = plt.subplots()

    ax.set_xlabel('Iterations', color='#1C2833')
    ax.set_ylabel('Accuracy', color='#1C2833')
    ax.grid()

    ax.plot(iterations, trainAccuracy, '-g')
    ax.plot(iterations, testAccuracy, '-r')

    plt.legend(["Train", "Test"], loc ="lower right")

    plt.show()


def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Generating hiperplane animations")

    # add arguments
    parser.add_argument('-i', dest='inputFile', required=False)
    parser.add_argument('-w', dest='weightsFile', required=False)
    parser.add_argument('-e', dest='errorFile', required=False)
    parser.add_argument('-test', dest='testFile', required=False)
    parser.add_argument('-train', dest='trainFile', required=False)

    args = parser.parse_args()

    INPUT_FILE = ''

    is2d = True

    print(args)
    if args.errorFile:
        print("Graphing error per iteration")
        iterations, errors = getErrorInputFromFile("output/" + args.errorFile)
        graphError(iterations, errors)
        exit(0)

    if args.testFile or args.trainFile:
        print("Graphing accuracy comparison")
        iterations, testAccuracy = getAccuracyInputFromFile("output/" + args.testFile)
        iterations, trainAccuracy = getAccuracyInputFromFile("output/" + args.trainFile)
        graphAccuracyComparison(iterations, trainAccuracy, testAccuracy)
        exit(0)

    if args.inputFile == EJ1_XOR:
        print("Hiperplane for data set ej1 XOR...")
        INPUT_FILE = "datasets/TP3-ej1-Conjuntoentrenamiento-xor.txt"
        DESIRED_FILE = "datasets/TP3-ej1-Salida-deseada-xor.txt"
    elif args.inputFile == EJ1_AND:
        print("Hiperplane for data set ej1 AND...")
        INPUT_FILE = "datasets/TP3-ej1-Conjuntoentrenamiento-and.txt"
        DESIRED_FILE = "datasets/TP3-ej1-Salida-deseada-and.txt"
    elif args.inputFile == EJ2:
        print("Hiperplane for data set ej 2...")
        INPUT_FILE = "datasets/TP3-ej2-Conjuntoentrenamiento.txt"
        DESIRED_FILE = "datasets/TP3-ej2-Salida-deseada.txt"
        is2d = False
    elif args.inputFile == EJ3:
        print("Cannot graph this input")
        exit(0)        

    inputs = getInputFromFile(INPUT_FILE)
    desired = getInputFromFile(DESIRED_FILE)

    WEIGHT_FILE = "output/" + args.weightsFile

    if is2d:
        hiperplanes = calculateR2Hiperplanes(WEIGHT_FILE)
        graphR2Hiperplane(inputs, desired, hiperplanes)
    else:
        hiperplanes = calculateR3Hiperplanes(WEIGHT_FILE)
        graphR3Hiperplane(inputs, desired, hiperplanes)

# call main
if __name__ == '__main__':
    main()

