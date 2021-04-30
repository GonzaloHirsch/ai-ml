import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pca import pca

INPUT_FILE = 'datasets/europe.csv'

# Extract and normalize data
df = pd.read_csv(INPUT_FILE, sep=',', header=0, index_col=0)
for i in range(df.shape[1]):
    # Get data to avoid ilocs
    data = df.iloc[:, i]
    # Calculate mean and std
    mean = np.mean(data)
    std = np.std(data)
    # Normalize
    df.iloc[:, i] = (data - mean)/std

# Calculate covariance
cov = np.cov(df.values)

# Calculate components
# pca = PCA(n_components=2)
# components = pca.fit_transform(cov)
# componentsDf = pd.DataFrame(data = components, columns = ['PC1', 'PC2'])

# fig, ax = plt.subplots()
# ax.scatter(x=componentsDf["PC1"], y=componentsDf["PC2"])
# plt.show()

model = pca(n_components=2)

# Fit transform
results = model.fit_transform(cov)

# Plot explained variance
# fig, ax = model.plot()

# Scatter first 2 PCs
# fig, ax = model.scatter()

# Make biplot with the number of features
fig, ax = model.biplot(n_feat=7)