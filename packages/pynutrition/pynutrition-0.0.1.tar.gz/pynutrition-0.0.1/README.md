# pynutrition
**LLM-driven Python daily nutrition app**

## Installation
```
pip install pynutrition
```

## Usage

```python
from pynutrition import Ingredient, Quantity, Calories, Composition
from pynutrition.nutrients import Fat, Saturates, Carbohydrate, Sugar, Protein, Salt

yoghurt = Ingredient(name="Greek Yoghurt Bakoma (5900197012723)", quantity=Quantity(250), calories=Calories(100), composition=Composition({
    Fat(7.5), Saturates(4.5), Carbohydrate(4.7), Sugar(4.7), Protein(3.5), Salt(0.12) 
}), base=100)
walnuts = Ingredient("Walnuts Carrefour (5905617004623)", Quantity(30), Calories(666), composition=Composition({
    Fat(60.3), Saturates(6.6), Carbohydrate(11.5), Sugar(9.9), Protein(16)
}), base=100)

meal = yoghurt + walnuts
print(meal.calories.as_int())  # round(2.5 * 100 + 0.3 * 666)
>>> 450
```

The `base` is used for calculations of nutritional information which are expressed as amounts per `base`,  often (as in the example) equal to 100g. All quantities are expressed in grams.

You can use `.get_data` and `.load_data` to fetch nutrional data with GPT-4 in the format accepted by the app and load each retrieved row as `Ingredient` that can be used to compose meals.

## Info

> Software engineers, plagued by the stereotype of poor eating and collecting bad habits

<small>Source: [HackerNoon](https://hackernoon.com/the-surprising-benefits-of-intermittent-fasting-for-software-engineers)</small>

This is a one-day project I quickly built (and tuned) for myself to improve my diet and nutrition. While you can see the haste in the code and design, I have realised even such rudimentary version might be useful to you. I want to contribute to supporting others in the community in their goal of becoming healthier, happier and stronger.


I hope I will find some time to make this project grow. If you are interested in extending its functionalities, found bugs or want to help, hit me up through [issues](https://github.com/haiyangdeperci/pynutrition/issues).
