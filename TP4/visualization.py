import matplotlib.patches as mptchs
import matplotlib.pyplot as plt
import numpy as np


def plot_kohonen_colormap(data, k=10, colormap='Blues', filename=None, addLabels = True):
    directory = 'graphs/'
    fig, ax = plt.subplots(figsize=(k, k))
    plt.pcolormesh(data, cmap=colormap, edgecolors=None)
    plt.colorbar()
    plt.xticks(np.arange(.5, float(k) + .5), range(k))
    plt.yticks(np.arange(.5, float(k) + .5), range(k))
    ax.set_aspect('equal')

    if addLabels:
        for (i, j), z in np.ndenumerate(data):
            ax.text(j + .5 , i + .5, round(z,2), ha='center', va='center')

    if filename:
        plt.savefig(directory + filename)
        plt.close()
        print(filename, " color map done!")
    else:
        plt.show()