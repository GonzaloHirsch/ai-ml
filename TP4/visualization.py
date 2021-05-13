import matplotlib.patches as mptchs
import matplotlib.pyplot as plt
import numpy as np


def plot_kohonen_colormap(data, k=10, colormap='Blues', filename=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.pcolormesh(data, cmap=colormap, edgecolors=None)
    plt.colorbar()
    plt.xticks(np.arange(.5, float(k) + .5), range(k))
    plt.yticks(np.arange(.5, float(k) + .5), range(k))
    ax.set_aspect('equal')

    if filename:
        plt.savefig(filename)
        plt.close()
        print("Kohonen color map done!")
    else:
        plt.show()