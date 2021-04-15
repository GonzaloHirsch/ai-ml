import parser
from perceptron import Perceptron

CONFIG_INPUT = "input/configuration.json"

def main():
    print("Parsing input data...")
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    trainingInput = parser.parseInput(config.input, True)
    labels = parser.parseInput(config.desired, False)
    # Create with shape because of N points of M components being NxM
    perceptron = Perceptron(trainingInput.shape[1], config.activation, config.learningRate)

    iterations = 0
    error = 1
                
    try:
        while iterations < config.iterations and error > config.error:
            print("Iteration #" + str(iterations))
            for inputs, label in zip(trainingInput, labels):

                summation = perceptron.summation(inputs)

                prediction = perceptron.activate(summation)

                perceptron.correctWeights(inputs, label, prediction, summation)

                error = perceptron.calculateError(label, prediction)
            iterations += 1

    except KeyboardInterrupt:
        print("Finishing up...")
    
    

# App entrypoint
if __name__ == "__main__":
    main()