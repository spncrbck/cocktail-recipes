import pandas as pd
import numpy as np

# drinks = ['mule', ['vodka', 1.5, 'ginger beer', 3, 'lime', 0.5], 'lime wedge', 'over ice', 'copper mug']

moscow_mule = [
    {
        'ingredients': [['vodka', 'ginger beer', 'lime'], [1.5, 3, 0.5], ['oz', 'oz', 'oz']],
        'garnish': 'lime wedge',
        'served': 'over ice',
        'vessel': 'copper mug'
    }
]

gin_and_tonic = [
    {
        'ingredients': [['gin', 'tonic water', 'lime'], [1.5, 3, 0.5], ['oz', 'oz', 'oz']],
        'garnish': 'lime wedge',
        'served': 'over ice',
        'vessel': 'highball glass'
    }
]

manhattan = [
    {
        'ingredients': [['rye', 'sweet vermouth', 'angostura bitters'], [2.5, 0.75, 2], ['oz', 'oz', 'dash']],
        'garnish': 'cherry',
        'served': 'neat',
        'vessel': 'coupe'
    }
]

recipes = [moscow_mule, gin_and_tonic, manhattan]

print(recipes)