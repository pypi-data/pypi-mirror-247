from dataclasses import dataclass, field
from typing import Self
from abc import ABCMeta
from pynutrition.utils import BaseNutritionalPrimitive

"""Symbols and categories can be used for an improved repr of objects."""

@dataclass(frozen=True)
class Nutrient(BaseNutritionalPrimitive, metaclass=ABCMeta):
    # proteins consist of amino acids
    # carbohydrates of sugar and fiber
    category: str = field(init=False, repr=False)

    def __new__(cls, *args, **kwargs): 
        if cls == Nutrient or cls.__bases__[0] == Nutrient: 
            raise TypeError("Cannot instantiate an abstract class.") 
        return super().__new__(cls)

    @property
    def name(self) -> str:
        return type(self).__name__.lower()

    @staticmethod
    def get_nutrient_categories():
        return Nutrient.__subclasses__()

    @staticmethod
    def get_all_nutrients():
        nutrients = []
        for category in Nutrient.get_nutrient_categories():
            nutrients.extend(category.__subclasses__())
        return nutrients


class NutrientMeta(ABCMeta):
    CATEGORY_ATTRIBUTE = "category"

    def __new__(cls, name, bases, dict):
        new = super().__new__(cls, name, bases, dict)
        if not hasattr(new, cls.CATEGORY_ATTRIBUTE):
            setattr(new, cls.CATEGORY_ATTRIBUTE, new)
        return new

@dataclass(frozen=True)
class Macronutrient(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class CarbohydrateNutrient(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class Mineral(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class Vitamin(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class FattyAcid(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class AminoAcid(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class OtherNutrient(Nutrient, metaclass=NutrientMeta): pass


@dataclass(frozen=True)
class Protein(Macronutrient): pass

@dataclass(frozen=True)
class Carbohydrate(Macronutrient):
    symbol: str = field(default="Carb", repr=False)

@dataclass(frozen=True)
class Fat(Macronutrient): pass

@dataclass(frozen=True)
class Fiber(CarbohydrateNutrient): pass

@dataclass(frozen=True)
class Sugar(CarbohydrateNutrient): pass

@dataclass(frozen=True)
class Calcium(Mineral):
    symbol: str = field(default="Ca", repr=False)

@dataclass(frozen=True)
class Iron(Mineral):
    symbol: str = field(default="Fe", repr=False)

@dataclass(frozen=True)
class Magnesium(Mineral):
    symbol: str = field(default="Mg", repr=False)

@dataclass(frozen=True)
class Phosphorus(Mineral):
    symbol: str = field(default="P", repr=False)

@dataclass(frozen=True)
class Potassium(Mineral):
    symbol: str = field(default="K", repr=False)

@dataclass(frozen=True)
class Sodium(Mineral):
    symbol: str = field(default="Na", repr=False)

class Salt():
    def __new__(cls, value: float) -> Self:
        return Sodium(value=cls.to_sodium(value))

    @staticmethod
    def to_sodium(value):
        return value / 2.5

@dataclass(frozen=True)
class Zinc(Mineral):
    symbol: str = field(default="Zn", repr=False)

@dataclass(frozen=True)
class Copper(Mineral):
    symbol: str = field(default="Cu", repr=False)

@dataclass(frozen=True)
class Manganese(Mineral):
    symbol: str = field(default="Mn", repr=False)

@dataclass(frozen=True)
class Selenium(Mineral):
    symbol: str = field(default="Se", repr=False)

@dataclass(frozen=True)
class VitaminC(Vitamin):
    symbol: str = field(default="Vit. C", repr=False)

@dataclass(frozen=True)
class Thiamin(Vitamin):
    symbol: str = field(default="B1", repr=False)

@dataclass(frozen=True)
class Riboflavin(Vitamin):
    symbol: str = field(default="B2", repr=False)

@dataclass(frozen=True)
class Niacin(Vitamin):
    symbol: str = field(default="B3", repr=False)

@dataclass(frozen=True)
class PantothenicAcid(Vitamin):
    symbol: str = field(default="B5", repr=False)

@dataclass(frozen=True)
class VitaminB6(Vitamin):
    symbol: str = field(default="B6", repr=False)

@dataclass(frozen=True)
class Folate(Vitamin):
    symbol: str = field(default="B9", repr=False)

@dataclass(frozen=True)
class Choline(OtherNutrient): pass

@dataclass(frozen=True)
class Betaine(AminoAcid): pass

@dataclass(frozen=True)
class VitaminB12(Vitamin):
    symbol: str = field(default="B12", repr=False)

### A ###

@dataclass(frozen=True)
class VitaminARae(Vitamin): pass

@dataclass(frozen=True)
class Retinol(Vitamin): pass

@dataclass(frozen=True)
class CaroteneBeta(Vitamin): pass

@dataclass(frozen=True)
class CaroteneAlpha(Vitamin): pass

@dataclass(frozen=True)
class CryptoxanthinBeta(Vitamin): pass

@dataclass(frozen=True)
class VitaminAIu(Vitamin): pass

@dataclass(frozen=True)
class Lycopene(Vitamin): pass

@dataclass(frozen=True)
class LuteinZeaxanthin(Vitamin): pass

### # ###

@dataclass(frozen=True)
class VitaminE(Vitamin):
    # AlphaTocopherol
    symbol: str = field(default="Vit. E", repr=False)

@dataclass(frozen=True)
class VitaminD(Vitamin):
    symbol: str = field(default="Vit. D", repr=False)

@dataclass(frozen=True)
class VitaminK(Vitamin):
    # Phylloquinone
    symbol: str = field(default="Vit. K", repr=False)

@dataclass(frozen=True)
class FattyAcidsTotalSaturated(FattyAcid): pass

Saturates = FattyAcidsTotalSaturated

@dataclass(frozen=True)
class FattyAcidsTotalMonounsaturated(FattyAcid): pass

@dataclass(frozen=True)
class FattyAcidsTotalPolyunsaturated(FattyAcid): pass

@dataclass(frozen=True)
class FattyAcidsTotalTrans(FattyAcid): pass

@dataclass(frozen=True)
class Cholesterol(OtherNutrient): pass

@dataclass(frozen=True)
class Tryptophan(AminoAcid): pass

@dataclass(frozen=True)
class Threonine(AminoAcid): pass

@dataclass(frozen=True)
class Isoleucine(AminoAcid): pass

@dataclass(frozen=True)
class Leucine(AminoAcid): pass

@dataclass(frozen=True)
class Lysine(AminoAcid): pass

@dataclass(frozen=True)
class Methionine(AminoAcid): pass

@dataclass(frozen=True)
class Cystine(AminoAcid): pass

@dataclass(frozen=True)
class Phenylalanine(AminoAcid): pass

@dataclass(frozen=True)
class Tyrosine(AminoAcid): pass

@dataclass(frozen=True)
class Valine(AminoAcid): pass

@dataclass(frozen=True)
class Arginine(AminoAcid): pass

@dataclass(frozen=True)
class Histidine(AminoAcid): pass

@dataclass(frozen=True)
class Alanine(AminoAcid): pass

@dataclass(frozen=True)
class AsparticAcid(AminoAcid): pass

@dataclass(frozen=True)
class GlutamicAcid(AminoAcid): pass

@dataclass(frozen=True)
class Glycine(AminoAcid): pass

@dataclass(frozen=True)
class Proline(AminoAcid): pass

@dataclass(frozen=True)
class Serine(AminoAcid): pass

@dataclass(frozen=True)
class AlcoholEthyl(OtherNutrient): pass

@dataclass(frozen=True)
class Caffeine(OtherNutrient): pass

@dataclass(frozen=True)
class Theobromine(OtherNutrient): pass
