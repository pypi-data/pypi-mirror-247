from dataclasses import dataclass, InitVar
from typing import Any, Self, Union, Optional
from pynutrition.utils import Quantity, Calories
from pynutrition.composition import Composition


class Diet:
    """Consists of meals, could be just Diet = [Meal, Meal, Meal, ...]
    + sum of calories and nutrients and (daily) diet summary generation"""
    NotImplemented


@dataclass
class Meal:
    calories: Calories
    composition: Composition
    ingredients: list["Ingredient"]


@dataclass
class Ingredient:
    name: str
    quantity: Quantity
    calories: Calories
    composition: Composition
    recommended_quantity: Optional[Quantity] = None
    base: Optional[InitVar[Union[float, int]]] = None

    def __post_init__(self):
        self @= (self.quantity / self.base if self.base is not None else Quantity(1))

    def _add(self, other: Union[Self, Meal]) -> Meal:
        ingredients = [self]
        ingredients.extend(other.ingredients) if isinstance(other, Meal) else ingredients.append(other)
        return Meal(
            calories=self.calories + other.calories,
            composition=self.composition + other.composition,
            ingredients=ingredients
        )

    def __radd__(self, other: Union[Self, Meal]) -> Meal:
        return self._add(other)
    
    def __add__(self, other: Union[Self, Meal]) -> Meal:
        return self._add(other)

    def measure(self, quantity: Quantity):
        self.calories @= quantity
        self.composition @= quantity
        return self