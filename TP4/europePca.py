import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt

INPUT_FILE = 'datasets/europe.csv'

# Extract and normalize data
df = pd.read_csv(INPUT_FILE, sep=',', header=0, index_col=0)

# Scale data due to large range differences
minMaxScaler = preprocessing.MinMaxScaler()
scaledDf = minMaxScaler.fit_transform(df)

# Standarize data to get mean=0 and std=1
standardScaler = preprocessing.StandardScaler()
standarizedDf = standardScaler.fit_transform(scaledDf)

# Calculate components
pca = PCA(n_components=2)
pcaFit = pca.fit(standarizedDf)
componentsDf = pd.DataFrame(data = np.transpose(pcaFit.components_), columns = ['PC1', 'PC2'])
componentsDf.index = np.array(df.columns)
print("\n------------------PRINCIPAL COMPONENTS------------------")
print(componentsDf)

# Calculate projections
projections = pcaFit.transform(standarizedDf)
valuesDf = pd.DataFrame(data = projections, columns = ['PC1', 'PC2'])
valuesDf.index = np.array(df.index)
print("\n------------------PROYECTIONS------------------")
print(valuesDf)

# Plotting the biplot (width, height)
plt.style.use('seaborn-bright')
fig, ax = plt.subplots(figsize=(12,7))
# Plot the horizontal bars
ax.barh(df.index, valuesDf["PC1"], align='center', color=['g' if val > 0 else 'r' for val in valuesDf["PC1"]])
ax.set_xlabel("PC1 (%{})".format(round(pcaFit.explained_variance_ratio_[0]*100, 2)))
# Add internal gridlines
major_ticks = np.arange(-4, 5.5, 0.5)
minor_ticks = np.arange(-4, 5.5, 0.25)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.25)
ax.grid(which='major', alpha=0.5)
ax.set_title("PCA for European Countries")
plt.show()

# Biplot
plt.style.use('seaborn-bright')
fig, ax = plt.subplots(figsize=(12,7))
# Calculate scaling factor for points
scalex = 1.0/(valuesDf["PC1"].max() - valuesDf["PC1"].min())
scaley = 1.0/(valuesDf["PC2"].max() - valuesDf["PC2"].min())
# Create scatter
ax.scatter(x=valuesDf["PC1"]*scalex, y=valuesDf["PC2"]*scaley)
# Add annotations
for i, txt in enumerate(np.array(df.index)):
    ax.annotate(txt, (valuesDf["PC1"][i]*scalex, valuesDf["PC2"][i]*scaley))
# Add feature vectors
for vec in zip(componentsDf["PC1"].values, componentsDf["PC2"].values):
    plt.quiver(0, 0, vec[0], vec[1], angles='xy', scale_units='xy', scale=1, color='r', width=0.001)
# Annotate feature vectors
for i, txt in enumerate(np.array(df.columns)):
    ax.annotate(txt, (componentsDf["PC1"][i], componentsDf["PC2"][i]), color='r')
# Add labels
ax.set_xlabel("PC1 (%{})".format(round(pcaFit.explained_variance_ratio_[0]*100, 2)))
ax.set_ylabel("PC2 (%{})".format(round(pcaFit.explained_variance_ratio_[1]*100, 2)))
# Add internal gridlines
major_ticks = np.arange(-0.6, 0.8, 0.1)
minor_ticks = np.arange(-0.6, 0.8, 0.05)
ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)
ax.grid(which='minor', alpha=0.25)
ax.grid(which='major', alpha=0.5)
ax.set_title("PCA for European Countries")
plt.show()