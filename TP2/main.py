# Lib imports
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import os
# Local imports
from character import Character
import inputParser as parser
from geneticAlgorithm import GeneticAlgorithm
from helper import getFitnessStats

# Variables pointing to configs
CONFIG_INPUT = "input/configuration.json"
DATA_OUTPUT = "output/output.csv"
OUTPUT_DIR = "output/"
OUTPUT_FIELDNAMES = ["generacion", "minimo", "promedio"]

# Function to run frame by frame
def animate(i):
    data = pd.read_csv(DATA_OUTPUT)
    x = data[OUTPUT_FIELDNAMES[0]]
    min = data[OUTPUT_FIELDNAMES[1]]
    avg = data[OUTPUT_FIELDNAMES[2]]
    plt.cla()
    plt.plot(x, min, 'r', label='Mínima', linewidth=2)
    plt.plot(x, avg, 'g', label='Promedio', linewidth=2)
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Fitness por Generación")
    plt.legend(loc='lower right')
    plt.tight_layout()

# Function to run the animation
def run_animation():
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), animate, interval=250)
    plt.tight_layout()
    plt.show()

# Makes sure the CSV file is prepared, create it if non existent
def prepareOutput():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(DATA_OUTPUT, 'w+') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
        csv_writer.writeheader()

# Writes a row of data to the output file
def writeRow(writer, gen, min, avg):
    info = {
        OUTPUT_FIELDNAMES[0]: gen,
        OUTPUT_FIELDNAMES[1]: min,
        OUTPUT_FIELDNAMES[2]: avg
    }
    writer.writerow(info)

def main(config):
    # Parse item files, pass the path to folder
    parser.parseItems(config.data)
    # Generate instance of the genetic algorithm configuration
    ga = GeneticAlgorithm(config)

    # Generate the initial random population
    population = ga.generateInitialPopulation(config.n)

    generation = 0
        
    # Iterate while terminal condition is not met
    while not ga.isTerminated(population):
        print('GENERATION #' + str(generation))
        # Calculate stats and write to file
        min, average = getFitnessStats(population)
        # Perform all with open file
        with open(DATA_OUTPUT, 'a') as csv_file:
            # Get instance of the writer
            csv_writer = csv.DictWriter(csv_file, fieldnames=OUTPUT_FIELDNAMES)
            writeRow(csv_writer, generation, min, average)
        # Select parents for next generation
        parents = ga.select(population, config.k, config.a)
        # Cross parents to generate children
        children = ga.crossAll(parents)
        # Mutate children
        for i in range(len(children)):
            children[i] = ga.mutate(children[i])
        # Select next generation
        population = ga.nextGeneration(population, children, config.b)
        generation += 1

    for p in population:
        print(p)
    
# App entrypoint
if __name__ == "__main__":
    # Parse configuration files
    config = parser.parseConfiguration(CONFIG_INPUT)
    # Prepare output file
    prepareOutput()

    # Create the thread for the processing
    x = threading.Thread(target=main, args=(config,))
    x.start()

    # Show plot if configured to
    if config.show:
        # Run animation on main thread
        run_animation()
