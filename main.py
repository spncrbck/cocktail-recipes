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
'''
def newRecipe():
    add_name = str(input("Waht is this drink called? "))
    add_ingredients()
    add_garnish = str(input("What is the garnish? "))
    add_served = str(input("How is it served? "))
    add_vessel = str(input("In what kind of glass or drinkware is it served? "))
    add_name = [
        {
            'ingredients': add_ingredients,
            'garnish': add_garnish,
            'served': add_served,
            'vessel': add_vessel
        }
    ]
    return recipes + add_name

def add_ingredients():
    ingredients_names = input("Please give ingredients in the form of a list of strings: ")
    ingredients_amounts = input("Please give ingredients amounts in the form of a list of floats: ")
    ingredients_units = input("Please give ingredient units in the form of a list of strings: ")
    return [ingredients_names, ingredients_amounts, ingredients_units]
'''

add_name = str(input("What is this drink called? "))
add_ingredients = [
    input("Please give ingredients in the form of a list of strings: "),
    input("Please give ingredients amounts in the form of a list of floats: "),
    input("Please give ingredient units in the form of a list of strings: ")
]
add_garnish = str(input("What is the garnish? "))
add_served = str(input("How is it served? "))
add_vessel = str(input("In what kind of glass or drinkware is it served? "))

add_name = [
    {
        'ingredients': add_ingredients,
        'garnish': add_garnish,
        'served': add_served,
        'vessel': add_vessel
    }
]

recipes + add_name

print(recipes[-1])