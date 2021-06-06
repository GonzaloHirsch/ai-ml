import matplotlib.pyplot as plt


def plotLatentSpace(latentPoints):
    x = [point[0] for point in latentPoints]
    y = [point[1] for point in latentPoints]
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, cmap='viridis')
    plt.show()