from matplotlib.pyplot import subplots, pcolormesh, colorbar, xticks, yticks, savefig, close, show
from numpy import arange, ndenumerate


def plot_kohonen_colormap(data, k=10, colormap='Blues', filename=None, addLabels = True):
    directory = 'graphs/'
    fig, ax = subplots(figsize=(k, k))
    pcolormesh(data, cmap=colormap, edgecolors=None)
    colorbar()
    xticks(arange(.5, float(k) + .5), range(k))
    yticks(arange(.5, float(k) + .5), range(k))
    ax.set_aspect('equal')

    if addLabels:
        for (i, j), z in ndenumerate(data):
            ax.text(j + .5 , i + .5, round(z,2), ha='center', va='center', c='r')

    if filename:
        savefig(directory + filename)
        close()
        print(filename, " color map done!")
    else:
        show()