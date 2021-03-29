# Lib imports
import pandas as pd
import matplotlib.pyplot as plt
# Local imports
import inputParser as parser
from geneticAlgorithm import GeneticAlgorithm
from helper import getFitnessStats, getDiversityStats, getBestCharacter

# Variables pointing to configs
CONFIG_INPUT = "input/configuration.json"
mins, avgs, divs, gens = [], [], [], []

def plotPoints(axes, fig, sampling):
    axes[0].clear()
    axes[1].clear()
    axes[0].plot(gens, mins, 'r', label='Mínima', linewidth=2)
    axes[0].plot(gens, avgs, 'g', label='Promedio', linewidth=2)
    axes[0].legend(loc='lower right')
    axes[0].plot(gens[-1], avgs[-1], 'ko', linewidth=2)
    axes[0].set_xlabel("Generación")
    axes[0].set_ylabel("Fitness")
    axes[0].set_title("Fitness por Generación")
    axes[0].text(gens[-1], avgs[-1],round(avgs[-1],2))
    axes[1].plot(gens, divs, 'r', label='Diversidad', linewidth=2)
    axes[1].legend(loc='lower left')
    axes[1].plot(gens[-1], divs[-1], 'ko', linewidth=2)
    axes[1].set_xlabel("Generación")
    axes[1].set_ylabel("Cantidad de Personajes Únicos")
    axes[1].set_title("Diversidad por Generación")
    axes[1].text(gens[-1], divs[-1], divs[-1])
    fig.tight_layout()
    plt.pause(sampling)

def prepareForPlot(population, generation, fig, axes, sampling):
    # Calculate stats and write to file
    min, average = getFitnessStats(population)
    diversity = getDiversityStats(population)
    mins.append(min)
    avgs.append(average)
    divs.append(diversity)
    gens.append(generation)
    # Plotting
    plotPoints(axes, fig, sampling)

def main():
    print("Parsing input data...")
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Parse item files, pass the path to folder
    parser.parseItems(config.data)
    # Generate instance of the genetic algorithm configuration
    ga = GeneticAlgorithm(config)
    print("Starting algorithm")
    print("Press ctrl + c to stop at any moment")

    # Generate the initial random population
    population = ga.generateInitialPopulation(config.n)

    generation = 0

    # Plotting
    if config.show:
        plt.style.use('fivethirtyeight')
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
        
    try:
        # Iterate while terminal condition is not met
        while not ga.isTerminated(population):
            print('GENERATION #' + str(generation))
            if config.show:
                prepareForPlot(population, generation, fig, axes, config.sampling)
            # Select parents for next generation
            parents = ga.select(population, config.k, config.a, generation)
            # Cross parents to generate children
            children = ga.crossAll(parents)
            # Mutate children
            for i in range(len(children)):
                children[i] = ga.mutate(children[i])
            # Select next generation
            population = ga.nextGeneration(population, children, config.b, generation)
            generation += 1

        if config.show:
            prepareForPlot(population, generation, fig, axes, config.sampling)

        print("Best configuration is:")
        print(getBestCharacter(population))

        if config.show:
            print("Close the plot to stop program")
            plt.show()
    except KeyboardInterrupt:
        print("Finishing up...")
    
# App entrypoint
if __name__ == "__main__":
    main()
