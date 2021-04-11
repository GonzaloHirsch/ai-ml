# Lib imports
import numpy as np
import json
# Local imports
from constants import FILES, ConfigOptions

# Function to parse a file and split and store contents
# Returns a np.array with all data
def parseInput(filepath, addExtraInput = False):
    with open(filepath) as f:
        # Read all lines
        lines = f.readlines()
        data = []
        for line in lines:
            if addExtraInput:
                data.append(np.array([1.0] + [float(elem) for elem in line.strip().split()]))
            else:
                data.append(np.array([float(elem) for elem in line.strip().split()]))
    return np.array(data)

# Parses the configuration
def parseConfiguration(configPath):
    with open(configPath) as json_file:
        data = json.load(json_file)
        
        # Get submaps inside config
        files = data[FILES]
        inputData = data[ConfigOptions.INPUT_DATA.value]
        desiredData = data[ConfigOptions.DESIRED_DATA.value]
        iterations = data[ConfigOptions.ITERATIONS.value]
        activation = data[ConfigOptions.ACTIVATION.value]
        learningRate = data[Config.LEARNING_RATE.value]
        multilayer = data[Config.MULTILAYER.value]
        
        # Create config
        config = Config(
            input=inputData,
            desired=desiredData,
            iterations=iterations,
            activation=activation,
            learningRate=learningRate,
            multilayer=multilayer 
        )
    return config