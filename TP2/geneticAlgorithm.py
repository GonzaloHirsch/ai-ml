# Local imports
from methods.mutacion import Mutacion
from character import Character

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.mutacion = Mutacion(config.mutacion)

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Generates an initial random population
    def generateInitialPopulation(self, n):
        characters = []
        for i in range(n):
            characters.append(Character.generateRandomCharacter())
        return characters

    def mutate(self, character):
        return self.mutacion.apply(character)