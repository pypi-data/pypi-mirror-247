from pynutrition.nutrients import Nutrient
from pynutrition.utils import Quantity
from typing import Optional, Sequence, Self
from sortedcontainers import SortedDict


class Composition:
    CATEGORIES = {category: idx for idx, category in enumerate(Nutrient.get_nutrient_categories())}
    def __init__(self, nutrients: Optional[list[Nutrient]] = None) -> None:
        # implemented as dict internally to solve a problem of different instances of the same class
        # in the form {Sodium: Sodium(0.5), ...}
        # exposing set-like API with minor modifications
        # might actually later be implemented as a vector to make things easier & faster
        self.store = SortedDict(lambda item: self.order(item))
        if nutrients is not None:
            self.update(nutrients)

    @staticmethod
    def order(item: Nutrient) -> tuple[int, str]:
        return (Composition.CATEGORIES[item.category], item.__name__.lower())
    
    def __repr__(self) -> str:
        s = ", ".join([str(item) for item in self.store.values()])
        return f"{{{s}}}"

    def __len__(self) -> int:
        return len(self.store)
    
    def add(self, elem: Nutrient) -> None:
        cls = type(elem)
        if cls in self.store:
            self.store[cls] += elem
        else:
            self.store[cls] = elem
    
    def update(self, *others: Sequence[Nutrient]) -> None:
        _update = []
        for other in others:
            _update.extend(zip([type(nutrient) for nutrient in other], other))
        self.store.update(_update)
    
    def pop(self) -> Nutrient:
        _, nutrient = self.store.popitem()
        return nutrient

    def discard(self, elem) -> None:
        try:
            del self.store[type(elem)]
        except KeyError:
            pass
    
    def copy(self):
        """Return a shallow copy of a composition"""
        new = Composition()
        new.store = self.store.copy()
        return new
    
    def __mul__(self, other: Quantity) -> Self:
        composition = self.copy()
        for key in composition:
            composition.store[key] *= other
        return composition

    def __add__(self, other: Self):
        # this can be better
        new = Composition()
        # here instead of costly conversion to set one can add a key
        # to a created SortedSet to avoid TypeError:
        # '<' not supported between instances of 'NutrientMeta' and 'NutrientMeta'
        # as handled in .__init__ and .order
        self = self.copy()
        other = other.copy()

        for key in set(self.store.keys()) - set(other.store.keys()):
            new.add(self.store.pop(key))

        for key in set(other.store.keys()) - set(self.store.keys()):
            new.add(other.store.pop(key))

        for key in self.store:
            new.add(self.store[key] + other.store[key])
        
        return new

    def measure(self, quantity: "Quantity"):
        return self * quantity
    
    def __iter__(self):
        return iter(self.store)

    def __eq__(self, __value: object) -> bool:
        return type(self) == type(__value) and all(own == other for own, other in zip(self, __value))
