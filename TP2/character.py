# Lib imports
import math  
# Local imports
from constants import Qualities, Clase, ItemTypes
from items import Items
from config import Config

class Character:
    INSTANCES = 0
    def __init__(self, clase, arma, botas, casco, guantes, pechera, height):
        self.id = Character.INSTANCES
        
        self.fitnessFunction = self.__getFitnessMethod(clase)
        self.fitness = 0

        self.gene = [arma, botas, casco, guantes, pechera, height]
        
        self.qualities = {
            Qualities.FU.value: 0, 
            Qualities.AG.value: 0,
            Qualities.EX.value: 0,
            Qualities.RE.value: 0,
            Qualities.VI.value: 0,
        }

        Character.INSTANCES += 1

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

    # -----------------------------------------------------------------
    # FITNESS FUNCTIONS
    # -----------------------------------------------------------------

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
            Clase.GUERRERO.value: self.__getWarriorFitness, 
            Clase.ARQUERO.value: self.__getArcherFitness, 
            Clase.DEFENSOR.value: self.__getDefendorFitness, 
            Clase.INFILTRADO.value: self.__getSpyFitness
        }
        return fitnessMethod[clase]

    # -----------------------------------------------------------------
    # RANDOM CHARACTER FUNCTIONS
    # -----------------------------------------------------------------

    @staticmethod
    def generateRandomCharacter():
        # Get instance of classes
        items = Items.getInstance()
        config = Config.getInstance()
        # Generate all items for new character
        gen = []
        for item in ItemTypes:
            if item != ItemTypes.ALTURA:
                gen.append(items.getRandomItem(item))
            else:
                gen.append(items.getRandomHeight())
        # Return character, generated items should be in correct positions
        return Character(config.clase, gen[0], gen[1], gen[2], gen[3], gen[4], gen[5])

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    def __str__(self):
        return '%s{%s\n}' % (
            type(self).__name__,
            ', '.join('\n\t%s = %s' % item for item in vars(self).items())
        )
    
