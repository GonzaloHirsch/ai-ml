# Lib imports
import random
from math import ceil, exp
import numpy as np
import heapq
from itertools import count
import bisect
# Local imports
from constants import Seleccion as SeleccionEnum, ConfigOptions
from helper import getRelativeFitnesses

class Seleccion:
    def __init__(self, sel, extra = None):
        self.sel = sel
        self.seleccion = self.__getSeleccionFunction(sel)
        self.extra = extra

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
        return bisect.bisect_left(accumulated, ri)

    def __getPseudoFitnessByRank(n, k):
        return (n - k)/n

    def __getBoltzmannTemperature(temp0, tempC, k, gen):
        # T = Tc + (T0 - Tc)*e^-k*gen
        return tempC + (temp0 - tempC)*exp(-1 * k * gen)

    def __getPseudoFitnessBoltzmann(chs, temperature):
        # e^(f(i) / T) pseudo-fitness
        fitnesses = np.array([exp(chr.fitness / temperature) for chr in chs])
        # mean value
        avgFitness = np.mean(fitnesses)
        # return e^(f(i) / T) / avgFitness
        return np.array([fitness / avgFitness for fitness in fitnesses])

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

    def __seleccionElite(self, chs, k, gen):
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


    def __seleccionRuleta(self, chs, k, gen):
        # Store the fitness of the characters in an array
        fitnesses = np.array([ch.fitness for ch in chs])
        return Seleccion.__seleccionRuletaInternal(chs, fitnesses, k)
        

    def __seleccionUniversal(self, chs, k, gen):
        # Store the fitness of the characters in an array
        fitnesses = np.array([ch.fitness for ch in chs])
        result = []

        # Calculated the accumulated relative fitnesses
        accumulated = np.cumsum(getRelativeFitnesses(fitnesses))

        # Create K random ri values between 0 and 1
        # And get the position in the accumulated array of each r value
        for i in range(0, k):
            ri = (random.uniform(0, 1) + i)/k
            idx = Seleccion.__getPositionInAccumulatedFitness(accumulated, ri)
            result.append(chs[idx])

        return result

    def __seleccionBoltzmann(self, chs, k, gen):
        # initial temperature
        temp0 = self.extra[ConfigOptions.T0.value]
        # base temperature
        tempC = self.extra[ConfigOptions.TBASE.value]
        # time constant of decay
        cteK = self.extra[ConfigOptions.K_DECAY.value]

        # get temperature
        temperature = Seleccion.__getBoltzmannTemperature(temp0, tempC, cteK, gen)
        
        # Get pseudo fitnesses
        fitnesses = Seleccion.__getPseudoFitnessBoltzmann(chs, temperature)

        return Seleccion.__seleccionRuletaInternal(chs, fitnesses, k)

    def __seleccionTorneoDeterminista(self, chs, k, gen):
        # number of characters to choose randomly
        m = self.extra[ConfigOptions.M_IND.value]

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

    def __seleccionTorneoProbabilistico(self, chs, k, gen):
        # treshold under which the best fitted character will be selected
        treshold = self.extra[ConfigOptions.THRESHOLD.value]

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

    def __seleccionRanking(self, chs, k, gen):
        n = len(chs)
        # Sort by fitness and convert to sorted list
        heap = Seleccion.__getSortedCharacters(chs)
        heaplist = [heapq.heappop(heap)[2] for i in range(n)]
        # Get pseudo fitnesses
        # Store the fitness of the characters in an array
        fitnesses = np.array([Seleccion.__getPseudoFitnessByRank(n, i + 1) for i in range(n)])
        return Seleccion.__seleccionRuletaInternal(heaplist, fitnesses, k)

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate the mutation
    # Receives: chs --> List of characters, k --> Amount to select
    def apply(self, chs, k, gen):
        return self.seleccion(chs, k, gen)

    def __getSeleccionFunction(self, sel):
        # Map with pointers to the functions
        selecciones = {
            SeleccionEnum.ELITE.value: self.__seleccionElite,
            SeleccionEnum.RULETA.value: self.__seleccionRuleta,
            SeleccionEnum.UNIVERSAL.value: self.__seleccionUniversal,
            SeleccionEnum.BOLTZMANN.value: self.__seleccionBoltzmann,
            SeleccionEnum.TORNEO_DET.value: self.__seleccionTorneoDeterminista,
            SeleccionEnum.TORNEO_PROB.value: self.__seleccionTorneoProbabilistico,
            SeleccionEnum.RANKING.value: self.__seleccionRanking
        }
        return selecciones[sel]

    
            
