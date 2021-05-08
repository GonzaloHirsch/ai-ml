import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt

INPUT_FILE = 'datasets/europe.csv'

# Extract and normalize data
df = pd.read_csv(INPUT_FILE, sep=',', header=0, index_col=0)

# Standarize data to get mean=0 and std=1
standardScaler = preprocessing.StandardScaler()
standarizedDf = standardScaler.fit_transform(df)

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
# Create scatter
ax.scatter(x=valuesDf["PC1"], y=valuesDf["PC2"])
# Add annotations
for i, txt in enumerate(np.array(df.index)):
    ax.annotate(txt, (valuesDf["PC1"][i], valuesDf["PC2"][i]))
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
ax.set_xticks(np.arange(-4, 5, 0.5))
ax.set_xticks(np.arange(-4, 5, 0.25), minor=True)
ax.set_yticks(np.arange(-3, 4, 0.5))
ax.set_yticks(np.arange(-3, 4, 0.25), minor=True)
ax.grid(which='minor', alpha=0.25)
ax.grid(which='major', alpha=0.5)
ax.set_title("PCA for European Countries")
plt.show()