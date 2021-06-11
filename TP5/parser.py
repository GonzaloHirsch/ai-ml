# Lib imports
from numpy import array
import json
# Local imports
from constants import FILES, LAYERS, ConfigOptions
from config import Config

# Function to parse a file and split and store contents
# Returns a np.array with all data
def parseInput(filepath):
    with open(filepath) as f:
        # Read all lines
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(array([1.0] + [float(elem) for elem in line.strip().split()]))
    return array(data)

# Parses the configuration
def parseConfiguration(configPath):
    with open(configPath) as json_file:
        data = json.load(json_file)
        
        # Get submaps inside config
        files = data[FILES]
        layers = data[LAYERS]
        # Get FILES data
        inputData = files[ConfigOptions.INPUT_DATA.value]
        # Get other data
        iterations = data[ConfigOptions.ITERATIONS.value]
        learningRate = data[ConfigOptions.LEARNING_RATE.value]
        momentum = data[ConfigOptions.MOMENTUM.value]        
        error = data[ConfigOptions.ERROR_LIMIT.value]
        beta = data[ConfigOptions.BETA.value]
        alpha = data[ConfigOptions.ALPHA.value]
        calculateMetrics = data[ConfigOptions.CALCULATE_METRICS.value]
        plotLatent = data[ConfigOptions.PLOT_LATENT.value]
        mode = data[ConfigOptions.MODE.value]
        generatorPoints = data[ConfigOptions.GENERATOR_POINTS.value]
        optimizer = data[ConfigOptions.OPTIMIZER.value]     
        noise = data[ConfigOptions.NOISE.value]  
        
        # Create config
        config = Config(
            inputs=inputData,
            iterations=iterations,
            learningRate=learningRate,
            momentum=momentum,
            error=error,
            layers=layers,
            beta=beta,
            alpha=alpha,
            calculateMetrics=calculateMetrics,
            plotLatent=plotLatent,
            mode=mode,
            generatorPoints=generatorPoints,
            optimizer=optimizer,
            noise=noise
        )
    return config