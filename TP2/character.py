# Lib imports
from math import tanh
from itertools import count
# Local imports
from constants import Qualities, Clase, ItemTypes, MULTIPLIERS
from items import Items
from config import Config

class Character:
    def __init__(self, clase, arma, botas, casco, guantes, pechera, height):
        # Determine fitness function
        self.calculateFitness = self.__getFitnessMethod(clase)
        self.fitness = 0
        self.computedHash = None

        self.genes = [arma, botas, casco, guantes, pechera, height]
        self.clase = clase
        
        self.qualities = {
            Qualities.FU.value: 0, 
            Qualities.AG.value: 0,
            Qualities.EX.value: 0,
            Qualities.RE.value: 0,
            Qualities.VI.value: 0,
        }

        # Calculate fitness & qualities
        self.calculateCompleteFitness()

    @staticmethod
    def fromList(clase, gene):
        return Character(clase, gene[0], gene[1], gene[2], gene[3], gene[4], gene[5])

    # -----------------------------------------------------------------
    # GENE FUNCTIONS
    # -----------------------------------------------------------------

    def setGene(self, itemType, newValue):
        self.genes[itemType.value] = newValue

    # -----------------------------------------------------------------
    # QUALITIES FUNCTIONS
    # -----------------------------------------------------------------

    def calculateCompleteFitness(self):
        self.calculateQualities()
        return self.calculateFitness()

    def calculateQualities(self):
        for quality in Qualities:
            self.qualities[quality.value] = self.__calculateQuality(quality)

    def __calculateQuality(self, quality):
        itemsValue = 0
        multiplier = MULTIPLIERS[quality.value]

        for idx in range(0, len(self.genes) - 1):
            itemsValue += self.genes[idx].values[quality.value]

        return multiplier * tanh(0.01 * itemsValue)

    # -----------------------------------------------------------------
    # ATTACK AND DEFENSE FUNCTIONS
    # -----------------------------------------------------------------

    def calculateAttackModifier(self):
        h = self.genes[-1]
        return 0.7 - (3 * h - 5)**4 + (3 * h - 5)**2 + h/4

    def calculateDefenseModifier(self):
        h = self.genes[-1]
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
        self.fitness = 0.6 * self.calculateAttack() + 0.6 * self.calculateDefense()
        return self.fitness

    def __getArcherFitness(self):
        self.fitness = 0.9 * self.calculateAttack() + 0.1 * self.calculateDefense()
        return self.fitness

    def __getDefendorFitness(self):
        self.fitness = 0.3 * self.calculateAttack() + 0.8 * self.calculateDefense()
        return self.fitness

    def __getSpyFitness(self):
        self.fitness = 0.8 * self.calculateAttack() + 0.3 * self.calculateDefense()
        return self.fitness

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
        gen = [items.getRandomItem(item) if item != ItemTypes.ALTURA else items.getRandomHeight() for item in ItemTypes]
        # Return character, generated items should be in correct positions
        return Character(config.clase, gen[0], gen[1], gen[2], gen[3], gen[4], gen[5])

    # -----------------------------------------------------------------
    # HELPER FUNCTIONS
    # -----------------------------------------------------------------

    def __str__(self):
        subs = 'fitness=%s => arma=%s, botas=%s, casco=%s, guantes=%s, pechera=%s, height=%s' % (self.fitness, self.genes[0].name, self.genes[1].name, self.genes[2].name, self.genes[3].name, self.genes[4].name, self.genes[5])
        s = '%s{%s}' % (type(self).__name__, subs)
        return s
    
    def __computeHashString(self):
        return hash((self.genes[0].name, self.genes[1].name, self.genes[2].name, self.genes[3].name, self.genes[4].name, round(self.genes[5], 2)))
        
    def __hash__(self):
        if self.computedHash == None:
            self.computedHash = self.__computeHashString()
        return self.computedHash
