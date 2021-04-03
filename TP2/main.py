# Lib imports
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import time
# Local imports
import inputParser as parser
from geneticAlgorithm import GeneticAlgorithm
from helper import getFitnessStats, getDiversityStats, getBestCharacter

# Variables pointing to configs
CONFIG_INPUT = "input/configuration.json"
OUTPUT_DIR = "output/"
OUTPUT_FIELDNAMES = ["generacion", "minimo", "promedio", "diversidad", "max"]
mins, avgs, divs, gens, maxs = [], [], [], [], []

# Makes sure the CSV file is prepared, create it if non existent
def prepareOutput(filename):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(filename, 'w+') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
        csv_writer.writeheader()

# Writes a row of data to the output file
def writeAll(writer):
    for i in range(len(gens)):
        info = {
            OUTPUT_FIELDNAMES[0]: gens[i],
            OUTPUT_FIELDNAMES[1]: mins[i],
            OUTPUT_FIELDNAMES[2]: avgs[i],
            OUTPUT_FIELDNAMES[3]: divs[i],
            OUTPUT_FIELDNAMES[4]: maxs[i]
        }
        writer.writerow(info)

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
    axes[0].text(gens[-1], avgs[-1] + 0.5, round(avgs[-1],2), horizontalalignment='right')
    axes[1].plot(gens, divs, 'r', label='Diversidad', linewidth=2)
    axes[1].legend(loc='lower left')
    axes[1].plot(gens[-1], divs[-1], 'ko', linewidth=2)
    axes[1].set_xlabel("Generación")
    axes[1].set_ylabel("Cantidad de Personajes Únicos")
    axes[1].set_title("Diversidad por Generación")
    axes[1].text(gens[-1], divs[-1] + 5, divs[-1])
    fig.tight_layout()
    plt.pause(sampling)

def storeData(population, generation):
    min, average, max = getFitnessStats(population)
    diversity = getDiversityStats(population)
    mins.append(min)
    avgs.append(average)
    divs.append(diversity)
    gens.append(generation)
    maxs.append(max)

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

    # Define output file and prepare output
    filename = OUTPUT_DIR + ('run_%s_%s.csv' % (config.clase, time.time()))
    prepareOutput(filename)

    # Generate the initial random population
    population = ga.generateInitialPopulation(config.n)

    generation = 0

    # Plotting
    if config.show:
        plt.style.use('seaborn-whitegrid')
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
        
    try:
        # Iterate while terminal condition is not met
        while not ga.isTerminated(population):
            print('GENERATION #' + str(generation))
            # Calculate data and keep in memory
            storeData(population, generation)
            # Plot the line
            if config.show:
                plotPoints(axes, fig, config.sampling)
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

        storeData(population, generation)
        if config.show:
            plotPoints(axes, fig, config.sampling)

        print("Best configuration is:")
        print(getBestCharacter(population))

        # Write output
        with open(filename, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
            writeAll(csv_writer)

        if config.show:
            print("Close the plot to stop program")
            plt.show()
    except KeyboardInterrupt:
        print("Finishing up...")
    
# App entrypoint
if __name__ == "__main__":
    main()
