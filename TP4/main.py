# Lib imports
# Local imports
from parser import parseConfiguration, parseInput
from methods import oja, kohonen, hopfield
from constants import NetworkOptions

CONFIG_INPUT = "input/configuration.json"

def main():
    # Parse configuration files
    config = parseConfiguration(CONFIG_INPUT)
    # Parse input
    inputs = parseInput(config.input, flatten=config.flatten)

    if config.network == NetworkOptions.OJA.value:
        oja.apply(config, inputs)
    elif config.network == NetworkOptions.KOHONEN.value:
        kohonen.apply(config, inputs)
    elif config.network == NetworkOptions.HOPFIELD.value:
        hopfield.apply(config, inputs)
    else:
        print("Invalid method \"{}\" chosen".format(config.network))

# App entrypoint
if __name__ == "__main__":
    main()