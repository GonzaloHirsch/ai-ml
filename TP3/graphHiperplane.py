import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = np.linspace(-2,2,100)

INPUT_FILE = "datasets/TP3-ej1-Conjuntoentrenamiento-xor.txt"
WEIGHTS_FILE = "output/run_input4_simple_0.02_1618538302.2997105.csv"

def calculateHiperplanes(filename):
    f = open(filename, 'r')

    iterativeHiperplanes = []
    index = 0
    for line in f:
        weights = line.lstrip("[").rstrip("]\n").split()
        if index > 0:
            print(weights)
            print(len(weights))
            if len(weights) != 3:
                print("Can only graph in 2D")
                exit(1)
            else:
                # Creating the y = mx + b function
                # Comes as a + by + cx = 0
                a = float(weights[0])
                b = float(weights[1])
                c = float(weights[2])
                if b != 0:
                    y = (c/(-1*b))*x + (a/(-1*b))
                else:
                    y = 0*x
                iterativeHiperplanes.append(y)

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

def graphR2Hiperplane(inputs, hiperplanes):
    fig, ax = plt.subplots()

    for coordinate in inputs:
        ax.plot(coordinate[0], coordinate[1], 'bo')
   
    ax.set_xlabel('x', color='#1C2833')
    ax.set_ylabel('y', color='#1C2833')
    ax.legend(loc='upper left')
    ax.grid()

    line, = ax.plot(x, hiperplanes[0], '-r', label='Iteration 0')

    def animate(i):
        print(i)
        if (i < len(hiperplanes)):
            line.set_ydata(hiperplanes[i])  # update the data.
        return line,

    ani = animation.FuncAnimation(
        fig, animate, interval=1000, blit=True, save_count=50)

    plt.show()

    # main() function
def main():
    inputs = getInputFromFile(INPUT_FILE)
    hiperplanes = calculateHiperplanes(WEIGHTS_FILE)

    graphR2Hiperplane(inputs, hiperplanes)

# call main
if __name__ == '__main__':
    main()

