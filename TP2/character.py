import numpy as np
import math  

from constants import Qualities
from constants import ClaseOptions


class Character:
    def __init__(self, clase, height, arma, botas, casco, guantes, pechera):

        self.fitness = self.__getFitnessMethod(clase)

        self.gene = [arma, botas, casco, guantes, pechera, height]
        
        self.qualities = {
            Qualities.FU.value: 0, 
            Qualities.AG.value: 0,
            Qualities.EX.value: 0,
            Qualities.RE.value: 0,
            Qualities.VI.value: 0,
        }

        # self.calculateQualities()


    # -----------------------------------------------------------------
    # QUALITIES FUNCTIONS
    # -----------------------------------------------------------------

    def calculateQualities(self):
        for quality in Qualities:
            self.qualities[quality.value] = self.__calculateQuality[quality.value]()


    def __getQualityMultiplier(self, quality):
        if Quality.FU == quality:
            return 100
        elif Quality.AG == quality:
            return 1
        elif Quality.EX == quality:
            return 0.6
        elif Quality.RE == quality:
            return 1
        elif Quality.VI == quality:
            return 100


    def __calculateQuality(self, quality):
        itemsValue = 0
        multiplier = self.__getQualityMultiplier(quality)

        for idx in range(1, len(self.gene)):
            itemsValue += self.gene[idx][quality]

        return multiplier * math.tanh(0.01 * itemsValue)

    # -----------------------------------------------------------------
    # ATTACK AND DEFENSE FUNCTIONS
    # -----------------------------------------------------------------

    def calculateAttackModifier(self):
        h = self.gene[len(self.gene)-1]
        return 0.7 - (3 * h - 5)**4 + (3 * h - 5)**2 + h/4

    def calculateDefenseModifier(self):
        h = self.gene[len(self.gene)-1]
        return 1.9 + (2.5 * h - 4.16)**4 + (2.5 * h - 4.16)**2 - (3*h)/10

    def calculateAttack(self):
        f = self.qualities[Qualities.FU.value]
        a = self.qualities[Qualities.AG.value]
        e = self.qualities[Qualities.EX.value]
        return (a + e) * f * self.calculateAttackModifier()

    def calculateDefense(self):
        r = self.qualities[Qualities.FU.value]
        e = self.qualities[Qualities.AG.value]
        v = self.qualities[Qualities.EX.value]
        return (r + e) * v * self.calculateDefenseModifier()


    def __getWarriorFitness(self):
        return 0.6 * self.calculateAttack() + 0.6 * self.calculateDefense()

    def __getArcherFitness(self):
        return 0.9 * self.calculateAttack() + 0.1 * self.calculateDefense()

    def __getDefendorFitness(self):
        return 0.3 * self.calculateAttack() + 0.8 * self.calculateDefense()

    def __getSpyFitness(self):
        return 0.8 * self.calculateAttack() + 0.3 * self.calculateDefense()

    
    def __getFitnessMethod(self, clase):

        fitnessMethod = {
            ClaseOptions.GUERRERO.value: self.__getWarriorFitness, 
            ClaseOptions.ARQUERO.value: self.__getArcherFitness, 
            ClaseOptions.DEFENSOR.value: self.__getDefendorFitness, 
            ClaseOptions.INFILTRADO.value: self.__getSpyFitness
        }
        return fitnessMethod[clase]

    
