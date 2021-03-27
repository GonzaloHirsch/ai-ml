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

    parents = ga.select(population, config.k, config.a)    

    print("BEFORE")
    print(parents[0])
    print(parents[1])

    n1, n2 = ga.cross(parents[0], parents[1])
    print("AFTER")
    print(n1)
    print(n2)


    # App flow
    # Generate initial population
    # Character.generateRandomCharacter()
    # While condition not met
    # Select parents
    # Cross
    # mutate
    # select next iteration
    

    
# App entrypoint
if __name__ == "__main__":
    main()
