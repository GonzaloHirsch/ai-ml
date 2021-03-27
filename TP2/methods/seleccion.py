# Lib imports
import random
from math import ceil
import numpy as np
import heapq
from itertools import count
# Local imports
from config import Config
from constants import Seleccion
from helper import getRelativeFitnesses

class Seleccion:
    def __init__(self, sel):
        self.sel = sel
        self.seleccion = self.selecciones[sel]

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    # Returns the amount of items per index to include in elite
    def __getEliteCount(n, k, i):
        return ceil((k - i)/n)

    # Returns a sorted character heap
    # Items are (fitness, pseudoindex, character)
    def __getSortedCharacters(chs):
        cnt = count(start=0, step=1)
        heap = [(ch.fitness * -1, next(cnt), ch) for ch in chs]
        heapq.heapify(heap)
        return heap

    def __getPositionInAccumulatedFitness(accumulated, ri):
        for i in range(0, len(accumulated)):
            if ri < accumulated[i]:
                return i
        return -1

    def __getPseudoFitnessByRank(n, k):
        return (n - k)/n

    # Internal roulette selection given the characters, fitnesses and k
    def __seleccionRuletaInternal(chs, fitnesses, k):
        result = []
        # Calculated the accumulated relative fitnesses
        accumulated = np.cumsum(getRelativeFitnesses(fitnesses))
        # Create K random ri values between 0 and 1
        # And get the position in the accumulated array of each r value
        for i in range(0, k):
            ri = random.uniform(0, 1)
            idx = Seleccion.__getPositionInAccumulatedFitness(accumulated, ri)
            result.append(chs[idx])
        return result

    # -----------------------------------------------------------------
    # SELECCION FUNCTIONS
    # -----------------------------------------------------------------

    def __seleccionElite(chs, k):
        n = len(chs)
        result = []
        # Sort characters
        heap = Seleccion.__getSortedCharacters(chs)
        i = 0
        count = 0
        while heap and count < k:
            # Keep only the character
            curr = heapq.heappop(heap)[2]
            # Get number of times to add
            subcount = Seleccion.__getEliteCount(n, k, i)
            # Add count times
            for _ in range(subcount):
                result.append(curr)
            count += subcount
            i += 1
        return result


    def __seleccionRuleta(chs, k):
        fitnesses = np.array([])
        # Store the fitness of the characters in an array
        for character in chs:
            fitnesses = np.append(fitnesses, character.fitness)
        return Seleccion.__seleccionRuletaInternal(chs, fitnesses, k)
        

    def __seleccionUniversal(chs, k):
        fitnesses = np.array([])
        result = []

        # Store the fitness of the characters in an array
        for character in chs:
            fitnesses = np.append(fitnesses, character.fitness)

        # Calculated the accumulated relative fitnesses
        accumulated = np.cumsum(getRelativeFitnesses(fitnesses))

        # Create K random ri values between 0 and 1
        # And get the position in the accumulated array of each r value
        for i in range(0, k):
            ri = (random.uniform(0, 1) + i)/k
            idx = Seleccion.__getPositionInAccumulatedFitness(accumulated, ri)
            result.append(chs[idx])

        return result

    def __seleccionBoltzmann(chs, k):
        return chs

    def __seleccionTorneoDeterminista(chs, k):
        # number of characters to choose randomly
        m = 2

        result = []
        for i in range(k):
            # choose the characters
            selectedChs = [random.choice(chs) for i in range(m)]
            bestCh = selectedChs[0]
            for ch in selectedChs:
                if ch.fitness > bestCh.fitness:
                    bestCh = ch
            result.append(bestCh)

        return result

    def __seleccionTorneoProbabilistico(chs, k):
        # treshold under which the best fitted character will be selected
        treshold = 0.75

        result = []
        for i in range(k):
            # choose the characters
            selectedChs = [random.choice(chs) for i in range(2)]

            # determine which character is selected
            r = random.uniform(0, 1)
            best = True
            if r > treshold:
                best = False

            # select the character
            selected = selectedChs[0]
            if selectedChs[0].fitness > selectedChs[1].fitness:
                selected = selectedChs[0] if best else selectedChs[1]
            else:
                selected = selectedChs[1] if best else selectedChs[0]
            
            result.append(selected)

        return result

    def __seleccionRanking(chs, k):
        n = len(chs)
        # Sort by fitness and convert to sorted list
        heap = Seleccion.__getSortedCharacters(chs)
        heaplist = [heapq.heappop(heap)[2] for i in range(n)]
        # Get pseudo fitnesses
        fitnesses = np.array([])
        # Store the fitness of the characters in an array
        for i in range(n):
            fitnesses = np.append(fitnesses, Seleccion.__getPseudoFitnessByRank(n, i + 1))
        return Seleccion.__seleccionRuletaInternal(heaplist, fitnesses, k)

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate the mutation
    # Receives: chs --> List of characters, k --> Amount to select
    def apply(self, chs, k):
        return self.seleccion(chs, k)

    # Map with pointers to the functions
    selecciones = {
        Seleccion.ELITE.value: __seleccionElite,
        Seleccion.RULETA.value: __seleccionRuleta,
        Seleccion.UNIVERSAL.value: __seleccionUniversal,
        Seleccion.BOLTZMANN.value: __seleccionBoltzmann,
        Seleccion.TORNEO_DET.value: __seleccionTorneoDeterminista,
        Seleccion.TORNEO_PROB.value: __seleccionTorneoProbabilistico,
        Seleccion.RANKING.value: __seleccionRanking
    }
            
