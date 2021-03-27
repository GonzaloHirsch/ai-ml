# Lib imports
from math import ceil, floor
import numpy as np
# Local imports
from methods.mutacion import Mutacion
from methods.seleccion import Seleccion
from methods.cruce import Cruce
from methods.corte import Corte
from methods.implementacion import Implementacion
from character import Character

class GeneticAlgorithm:
    def __init__(self, config):
        self.config = config
        self.mutacion = Mutacion(config.mutacion)
        self.seleccion1 = Seleccion(config.seleccion[0])
        self.seleccion2 = Seleccion(config.seleccion[1])
        self.reemplazo1 = Seleccion(config.reemplazo[0])
        self.reemplazo2 = Seleccion(config.reemplazo[1])
        self.cruce = Cruce(config.cruce)
        self.corte = Corte(config.corte)
        self.implementacion = Implementacion(config.implementacion)

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Generates an initial random population
    def generateInitialPopulation(self, n):
        characters = []
        for i in range(n):
            characters.append(Character.generateRandomCharacter())
        return characters

    def select(self, characters, k, a, gen):
        k1 = ceil(k * a)
        k2 = floor(k * (1 - a))
        list1 = self.seleccion1.apply(characters, k1, gen)
        list2 = self.seleccion2.apply(characters, k2, gen)
        return list1 + list2

    def mutate(self, character):
        return self.mutacion.apply(character)

    def crossAll(self, parents):
        n = len(parents)
        children = []
        for i in range(0, n, 2):
            if i + 1 >= n:
                children.append(parents[i])
            else:
                child1, child2 = self.cross(parents[i], parents[i+1])
                children.append(child1)
                children.append(child2)
        return children

    def cross(self, p1, p2):
        return self.cruce.apply(p1, p2)

    def nextGeneration(self, population, children, b, gen):
        return self.implementacion.apply(population, children, self.reemplazo1, self.reemplazo2, b, gen)

    def isTerminated(self, chs):
        return self.corte.apply(chs)