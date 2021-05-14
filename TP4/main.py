# Lib imports
# Local imports
from parser import parseConfiguration, parseInput
from methods import oja, kohonen, hopfield
from constants import NetworkOptions
from helper import createDirectoryIfNotExist

CONFIG_INPUT = "input/configuration.json"

def main():
    # Create directories to avoid errors
    createDirectoryIfNotExist("output/")
    createDirectoryIfNotExist("graphs/")
    # Parse configuration files
    config = parseConfiguration(CONFIG_INPUT)
    # Parse input
    inputs, inputNames = parseInput(config.input, flatten=config.flatten)

    if config.network == NetworkOptions.OJA.value:
        oja.apply(config, inputs)
    elif config.network == NetworkOptions.KOHONEN.value:
        kohonen.apply(config, inputs, inputNames)
    elif config.network == NetworkOptions.HOPFIELD.value:
        testInputs = parseInput(config.test, flatten=config.flatten)
        hopfield.apply(config, inputs, testInputs)
    else:
        print("Invalid method \"{}\" chosen".format(config.network))

# App entrypoint
if __name__ == "__main__":
    main()