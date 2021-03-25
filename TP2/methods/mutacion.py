# Lib imports
import random
# Local imports
from items import Items
from config import Config
from constants import ItemTypes

def mutacionCompleta(ch):
    # Recover instances
    items = Items.getInstance()
    conf = Config.getInstance()
    # Generate random number
    rnd = random.uniform(0, 1)
    # If less than probability, mutate
    if rnd <= conf.pm:
        # Iterate item types and get all new items
        for item in ItemTypes:
            # Get new random item for that type
            if item != ItemTypes.ALTURA:
                newItem = items.getRandomItem(item)
            else:
                newItem = items.getRandomHeight()
            # Set the gene in the character
            ch.setGene(item, newItem)

def mutacionGen(ch):
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
        # Set the gene in the character
        ch.setGene(item, newItem)
            
