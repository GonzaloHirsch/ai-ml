# Lib imports
from math import ceil, floor
import numpy as np
# Local imports
from methods.mutacion import Mutacion
from methods.seleccion import Seleccion
from character import Character

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.mutacion = Mutacion(config.mutacion)
        self.seleccion1 = Seleccion(config.seleccion[0])
        self.seleccion2 = Seleccion(config.seleccion[1])

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

    def select(self, characters, k, a):
        k1 = ceil(k * a)
        k2 = floor(k * (1 - a))
        list1 = self.seleccion1.apply(characters, k1)
        list2 = self.seleccion2.apply(characters, k2)
        return list1 + list2