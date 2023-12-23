# extentable as a load to DB
import pandas as pd
from pynutrition.diet import Ingredient
from pynutrition.composition import Composition
from pynutrition.utils import Quantity, Calories
import pynutrition.nutrients as nutrients

FIELDS = [
    'name',
    '',  # removed
    'calories',
    'carbohydrate',  # changed from carbs
    'fat',
    'protein',
    'fiber',
    'sugar',  # changed from sugars_total_including_nlea
    'calcium',
    'iron',
    'magnesium',
    'phosphorus',
    'potassium',
    'sodium',
    'zinc',
    'copper',
    'manganese',
    'selenium',
    'vitamin_c',
    'thiamin',
    'riboflavin',
    'niacin',
    'pantothenic_acid',
    'vitamin_b6',
    'folate',
    'choline',
    'betaine',
    'vitamin_b12',
    'vitamin_a_rae',
    'retinol',
    'carotene_beta',
    'carotene_alpha',
    'cryptoxanthin_beta',
    'vitamin_a_iu',
    'lycopene',
    'lutein_zeaxanthin',
    'vitamin_e',
    'vitamin_d',
    'vitamin_k',
    'fatty_acids_total_saturated',
    'fatty_acids_total_monounsaturated',
    'fatty_acids_total_polyunsaturated',
    'fatty_acids_total_trans',
    'cholesterol',
    'tryptophan',
    'threonine',
    'isoleucine',
    'leucine',
    'lysine',
    'methionine',
    'cystine',
    'phenylalanine',
    'tyrosine',
    'valine',
    'arginine',
    'histidine',
    'alanine',
    'aspartic_acid',
    'glutamic_acid',
    'glycine',
    'proline',
    'serine',
    'alcohol_ethyl',
]

def load_data(filename: str = "data/gpt_nutrition.csv") -> list[Ingredient]:
    ingredients = []
    for row in pd.read_csv(filename).to_numpy():
        composition = Composition()
        for field_name, value in zip(FIELDS[3:], row[3:]):
            composition.add(getattr(nutrients, "".join([part.title() for part in field_name.split("_")]), None)(float(value)))
        ingredients.append(Ingredient(name=row[0], quantity=Quantity(100), calories=Calories(float(row[2])), composition=composition))
    return ingredients
