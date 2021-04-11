import parser

CONFIG_INPUT = "input/configuration.json"

def main():
    print("Parsing input data...")
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    inputs = parser.parseInput(config.input, True)
    labels = parser.parseInput(config.desired, False)

    # Llamar a train

def train():
    # Nested for loops
        # summation
        # activation
        # correct weights
        # error
    return

# App entrypoint
if __name__ == "__main__":
    main()