import pytest

from pynutrition.diet import Ingredient
from pynutrition.nutrients import Fat, Saturates, Carbohydrate, Sugar, Protein, Salt, Sodium
from pynutrition.composition import Composition
from pynutrition.utils import Quantity, Calories


class TestMeal:
    def test_make_meal(self):
        yoghurt = Ingredient("Greek Yoghurt Bakoma (5900197012723)", Quantity(250), Calories(100), composition=Composition({
            Fat(7.5), Saturates(4.5), Carbohydrate(4.7), Sugar(4.7), Protein(3.5), Salt(0.12) 
        }), base=100)
        walnuts = Ingredient("Walnuts Carrefour (5905617004623)", Quantity(30), Calories(666), composition=Composition({
            Fat(60.3), Saturates(6.6), Carbohydrate(11.5), Sugar(9.9), Protein(16)
        }), base=100)
        actimel = Ingredient("Actimel (5900643045930)", Quantity(100), Calories(70), composition=Composition({
            Fat(1.4), Saturates(1.0), Carbohydrate(10.7), Sugar(10.6), Protein(2.8), Salt(0.1)
        }), base=100)

        meal = yoghurt + walnuts + actimel
        assert meal.calories != 836, "Calories should not be added without considering quantities"
        assert meal.calories == Calories(250/100 * 100 + 30/100 * 666 + 100/100 * 70) == Calories(519.8)
        assert meal.composition == Composition({
            Fat(2.5 * 7.5 + 0.3 * 60.3 + 1.4),
            Saturates(2.5 * 4.5 + 0.3 * 6.6 + 1),
            Carbohydrate(2.5 * 4.7 + 0.3 * 11.5 + 10.7),
            Sugar(2.5 * 4.7 + 0.3 * 9.9 + 10.6),
            Protein(2.5 * 3.5 + 0.3 * 16 + 2.8),
            Sodium(2.5 * (0.12 / 2.5) + (0.1 / 2.5))
        }) == Composition({Fat(38.24), Saturates(14.23), Carbohydrate(25.9), Sugar(25.32), Protein(16.35), Sodium(0.16)})
        
