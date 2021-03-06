import matplotlib.pyplot as plt
import numpy as np

def plotLatentSpace(latentPoints, labels):
    x = [point[0] for point in latentPoints]
    y = [point[1] for point in latentPoints]
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, cmap='viridis')

    if labels != None:
        for i in range(len(x)):
            plt.text(x=x[i] + 0.005, y=y[i] + 0.005, s=labels[i])
    plt.show()
    
def plotError(errorPoints):
    x = np.linspace(0, len(errorPoints), len(errorPoints))
    plt.plot(x, errorPoints)
    plt.xlabel("Pasos del Optimizador")
    plt.ylabel("Error Promedio")
    plt.show()