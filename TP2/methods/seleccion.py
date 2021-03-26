# Lib imports
import random
from math import ceil
import heapq
# Local imports
from config import Config
from constants import Seleccion

class Seleccion:
    def __init__(self, sel):
        self.sel = sel
        self.seleccion = self.selecciones[sel]

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    def __getEliteCount(n, k, i):
        return ceil((k - i)/n)

    # Returns a sorted character heap
    # Items are (fitness, id, character)
    def __getSortedCharacters(chs):
        heap = [(ch.fitness * -1, ch.id, ch) for ch in chs]
        heapq.heapify(heap)
        return heap

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
        return chs

    def __seleccionUniversal(chs, k):
        return chs

    def __seleccionBoltzmann(chs, k):
        return chs

    def __seleccionTorneoDeterminista(chs, k):
        return chs

    def __seleccionTorneoProbabilistico(chs, k):
        return chs

    def __seleccionRanking(chs, k):
        return chs

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
            
