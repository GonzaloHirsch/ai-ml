import parser
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"

def main():
    print("Parsing input data...")
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    trainingInput = parser.parseInput(config.input, True)
    labels = parser.parseInput(config.desired, False)
    perceptron = Perceptron(trainingInput.size, config.activation, config.learningRate)
                
    try:
        for _ in range(config.iterations):
            for inputs, label in zip(trainingInput, labels):
                summation = perceptron.summation(inputs)

                prediction = perceptron.activate(summation)

                perceptron.correctWeights(inputs, label, prediction, summation)
    except KeyboardInterrupt:
        print("Finishing up...")
    
    

# App entrypoint
if __name__ == "__main__":
    main()