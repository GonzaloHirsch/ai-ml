# Lib imports
from numpy import array
from json import load
from pandas import read_csv
from sklearn.preprocessing import StandardScaler
# Local imports
from constants import FILES, METHOD, ConfigOptions
from config import Config

# Function to parse a file and split and store contents
# Returns a np.array with all data
def parseInput(filepath, flatten = 1):
    # Asume that flatten is only for the last exercise
    if flatten > 1:
        with open(filepath) as f:
            # Read all lines
            lines = f.readlines()
            data = []
            subdata = []
            # Count rows for flattening
            rowCount = 0
            for line in lines:
                rowCount += 1
                # Append to sub data
                subdata = subdata + [int(elem) for elem in line.strip().split()]
                # Flatten the array
                if rowCount == flatten:
                    data.append(array(subdata).flatten())
                    subdata = []
                    rowCount = 0
            return array(data), None
    # Asume that not flatten is for pca
    else:
        df = read_csv(filepath, sep=',', header=0, index_col=0)
        standardScaler = StandardScaler()
        standarizedDf = standardScaler.fit_transform(df)
        return standarizedDf, array(df.index)

# Parses the configuration
def parseConfiguration(configPath):
    with open(configPath) as json_file:
        data = load(json_file)
        
        # Get submaps inside config
        files = data[FILES]
        method = data[METHOD]
        # Get FILES data
        inputData = files[ConfigOptions.INPUT_DATA.value]
        testData = files[ConfigOptions.TEST_DATA.value]
        flatten = files[ConfigOptions.FLATTEN_DATA.value]
        # Get METHOD data
        network = method[ConfigOptions.NETWORK_METHOD.value]
        k = method[ConfigOptions.K_SIZE_METHOD.value]
        # Get other data
        iterations = data[ConfigOptions.ITERATIONS.value]
        learningRate = data[ConfigOptions.LEARNING_RATE.value]
        
        # Create config
        config = Config(
            input=inputData,
            test=testData,
            flatten=flatten,
            network=network,
            k=k,
            iterations=iterations,
            learningRate=learningRate
        )
    return config