# Lib imports
import pandas as pd
import os
import json
# Local imports
from constants import ItemFiles, ConfigOptions
from items import Items
from config import Config

# Function to parse all the items in the files
def parseItems(directoryPath):
    # Array to hold all the information
    data = []
    # Iterate and extract the files
    for itemFile in ItemFiles:
        # Parse file
        df = pd.read_csv(os.path.join(directoryPath, itemFile.value), sep='\t', header=0, index_col=0)
        # Push dataframe to array
        data.append(df)
    # Generate new items class
    Items.setInstance(data)

# Parses the configuration
def parseConfiguration(configPath):
    with open(configPath) as json_file:
        data = json.load(json_file)
        # Get submaps inside config
        gen = data[ConfigOptions.GEN.value]
        nums = data[ConfigOptions.NUMS.value]
        # Create config
        config = Config(
            clase=data[ConfigOptions.CLASE.value], 
            data=data[ConfigOptions.DATA.value], 
            cruce=gen[ConfigOptions.CRUCE.value], 
            mutacion=gen[ConfigOptions.MUTACION.value], 
            seleccion=gen[ConfigOptions.SELECCION.value], 
            reemplazo=gen[ConfigOptions.REEMPLAZO.value], 
            implementacion=gen[ConfigOptions.IMPLEMENTACION.value], 
            corte=gen[ConfigOptions.CORTE.value], 
            a=nums[ConfigOptions.A.value], 
            b=nums[ConfigOptions.B.value], 
            n=nums[ConfigOptions.N.value], 
            k=nums[ConfigOptions.K.value],
            pm=nums[ConfigOptions.PM.value],
            crit1=nums[ConfigOptions.CRITERIO_1.value],
            crit2=nums[ConfigOptions.CRITERIO_2.value]
        )
    return config