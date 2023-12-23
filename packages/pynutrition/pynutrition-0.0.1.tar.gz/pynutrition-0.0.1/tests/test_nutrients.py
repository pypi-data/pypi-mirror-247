import pytest

from pynutrition.nutrients import Nutrient, Fat, Carbohydrate

class TestNutrients:
    def test_nutrient_addition(self):
            fat_1, fat_2, fat_3 = Fat(1), Fat(2), Fat(3)
            carbohydrate = Carbohydrate(5)
            with pytest.raises(TypeError):
                fat_1 + carbohydrate
            assert fat_1 + fat_2 == fat_3
            assert fat_1.value == 1
            assert fat_2.value == 2
            assert fat_3.value == 3
