from dataclasses import dataclass, InitVar, field
from typing import Union, Self, Optional, Callable
from operator import add as op_add, mul as op_mul, truediv as op_div
from abc import ABC


@dataclass(frozen=True)
class BaseNutritionalPrimitive(ABC):
    value: Union[float, int]
    # Base for nutrients in grams, possibly this can be offloaded elsewhere
    base: Optional[InitVar[Union[float, int]]] = None

    def __post_init__(self, base: Optional[Union[float, int]]=base):
        if base is not None:
            self._value_at_base = self.value
            # standardize to 1 gram
            self.value /= base
    
    def act(self, other: Union[Self, int, float], operation: Callable) -> Self:
        cls = type(self)
        if isinstance(other, (int, float)):
            return cls(value=operation(self.value, other))
        elif isinstance(other, Quantity):
            return cls(value=operation(self.value, other.value))
        elif isinstance(other, cls):
            return cls(value=operation(self.value, other.value))
        raise TypeError(f"Instance {other} is not of type {cls}, int, float")

    def __add__(self, other: Union[Self, int, float]) -> Self:
        return self.act(other, op_add)

    def __mul__(self, other: Union[Self, int, float]) -> Self:
        return self.act(other, op_mul)

    def as_int(self):
        return round(self.value)

    @property
    def at_base(self):
        if hasattr(self, "_value_at_base"):
            return self._value_at_base
    
    def measure(self, quantity: "Quantity"):
        return self * quantity


@dataclass
class Quantity:
    "Wrapper handling operations on nutrients"
    value: Union[float, int]

    def __matmul__(self, other: BaseNutritionalPrimitive):
        return other.measure(quantity=self)
    def __rmatmul__(self, other: BaseNutritionalPrimitive):
        return self.__matmul__(other)

    def __truediv__(self, other: Union[Self, int, float]) -> Self:
        if isinstance(other, type(self)):
            return Quantity(self.value / other.value)
        return Quantity(self.value / other)

@dataclass(frozen=True)
class Calories(BaseNutritionalPrimitive): pass
