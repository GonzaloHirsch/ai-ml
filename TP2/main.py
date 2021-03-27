# Local imports
from character import Character
import inputParser as parser
from geneticAlgorithm import GeneticAlgorithm

# Variables pointing to configs
CONFIG_INPUT = "input/configuration.json"

def main():
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse item files, pass the path to folder
    parser.parseItems(config.data)
    # Generate instance of the genetic algorithm configuration
    ga = GeneticAlgorithm(config)

    # Generate the initial random population
    population = ga.generateInitialPopulation(config.n)

    # Iterate while terminal condition is not met
    while not ga.isTerminated(population):
        # Select parents for next generation
        parents = ga.select(population, config.k, config.a)
        # Cross parents to generate children
        children = ga.crossAll(parents)
        # Mutate children
        for i in range(len(children)):
            children[i] = ga.mutate(children[i])
        # Select next generation
        population = ga.nextGeneration(population, children, config.n, config.k, config.b)
    
# App entrypoint
if __name__ == "__main__":
    main()
