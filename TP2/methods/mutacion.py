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

    # -----------------------------------------------------------------
    # MUTACION FUNCTIONS
    # -----------------------------------------------------------------

    def __mutacionCompleta(ch):
        # Recover instances
        items = Items.getInstance()
        conf = Config.getInstance()
        # Generate random number
        rnd = random.uniform(0, 1)
        # If less than probability, mutate
        if rnd <= conf.pm:
            # Generate copy of items
            genes = list.copy(ch.gene)
            # Iterate item types and get all new items
            for item in ItemTypes:
                # Get new random item for that type
                if item != ItemTypes.ALTURA:
                    newItem = items.getRandomItem(item)
                else:
                    newItem = items.getRandomHeight()
                genes[item.value] = newItem
            # Create new character instance
            ch = Character.fromList(ch.clase, genes)
        return ch

    def __mutacionGen(ch):
        # Recover instances
        items = Items.getInstance()
        conf = Config.getInstance()
        # Generate random number
        rnd = random.uniform(0, 1)
        # If less than probability, mutate
        if rnd <= conf.pm:
            # Generate a random property to alter
            rnd = int(random.uniform(0, len(ItemTypes)))
            # Get item for that index
            item = ItemTypes(rnd)
            # Generate random item
            if item != ItemTypes.ALTURA:
                newItem = items.getRandomItem(item)
            else:
                newItem = items.getRandomHeight()
            # Generate gene copy
            genes = list.copy(ch.gene)
            # Set the gene in the new genes
            genes[item.value] = newItem
            # Generate new character instance
            ch = Character.fromList(ch.clase, genes)
        return ch

    def __mutacionLimitada(ch):
        return ch

    def __mutacionUniforme(ch):
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
            
