# Lib imports
import random
# Local imports
from items import Items
from config import Config
from constants import ItemTypes, Mutacion
from character import Character

class Mutacion:
    def __init__(self, mut):
        self.mut = mut
        self.mutacion = self.mutaciones[mut]

    def __getRandomGene(geneIdx):
        items = Items.getInstance()
        # Get item for that index
        item = ItemTypes(geneIdx)
        # Generate random item
        if item != ItemTypes.ALTURA:
            newItem = items.getRandomItem(item)
        else:
            newItem = items.getRandomHeight()

        return newItem

    # -----------------------------------------------------------------
    # MUTACION FUNCTIONS
    # -----------------------------------------------------------------

    def __mutacionCompleta(ch):
        # Recover instances
        conf = Config.getInstance()
        # Generate random number
        rnd = random.uniform(0, 1)
        # If less than probability, mutate
        if rnd <= conf.pm:
            # Generate copy of items
            genes = [*ch.rawGenes]
            # Iterate item types and get all new items
            for idx in range(0, len(genes)):
                genes[idx] = Mutacion.__getRandomGene(idx)
            # Create new character instance
            ch = Character.fromList(ch.clase, genes)
        return ch

    def __mutacionGen(ch):
        # Recover instances
        conf = Config.getInstance()
        # Generate random number
        rnd = random.uniform(0, 1)
        # If less than probability, mutate
        if rnd <= conf.pm:
            # Generate a random property to alter
            geneIdx = int(random.uniform(0, len(ItemTypes)))
            # Generate gene copy
            genes = [*ch.rawGenes]
            # Set the gene in the new genes
            genes[geneIdx] = Mutacion.__getRandomGene(geneIdx)
            # Generate new character instance
            ch = Character.fromList(ch.clase, genes)
        return ch

    def __mutacionLimitada(ch):

        # Recover instances
        conf = Config.getInstance()

        M = len(ch.genes) + 1
        # Generate random number
        rnd = random.uniform(0, 1)
        # If less than probability, mutate
        if rnd <= conf.pm:
            # Generate a random amount of genes to alter between 1 and M
            amountToAlter = int(random.uniform(1, M))
            # Idx of gene to be altered
            genesToAlter = random.sample(range(0, len(ch.genes)), amountToAlter)
            # Generate gene copy
            genes = [*ch.rawGenes]
            
            for geneIdx in genesToAlter:
                # Set the gene in the new genes
                genes[geneIdx] = Mutacion.__getRandomGene(geneIdx)

            # Generate new character instance
            ch = Character.fromList(ch.clase, genes)
            
        return ch

    def __mutacionUniforme(ch):

        # Recover instances
        conf = Config.getInstance()

        # Generate copy of items
        genes = [*ch.rawGenes]

        # Iterate item types
        for idx in range(0, len(genes)):
            rnd = random.uniform(0, 1)
            # If less than probability, mutate
            if rnd <= conf.pm:
                genes[idx] = Mutacion.__getRandomGene(idx)

        # Create new character instance
        ch = Character.fromList(ch.clase, genes)

        return ch

    # -----------------------------------------------------------------
    # EXPOSED FUNCTIONS
    # -----------------------------------------------------------------

    # Exposed method to calculate the mutation
    def apply(self, ch):
        return self.mutacion(ch)

    # Map with pointers to the functions
    mutaciones = {
        Mutacion.GEN.value: __mutacionGen, 
        Mutacion.LIMITADA.value: __mutacionLimitada, 
        Mutacion.UNIFORME.value: __mutacionUniforme,
        Mutacion.COMPLETA.value: __mutacionCompleta
    }
            
