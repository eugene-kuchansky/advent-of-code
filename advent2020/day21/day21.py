import sys
from typing import List, Iterable, Optional, NamedTuple, Set, Tuple, Iterator, Dict


class Food(NamedTuple):
    allergens: Set[str]
    ingredients: Set[str]

    @staticmethod
    def parse(line: str) -> "Food":
        line = line[:-1]
        ingredients_list, allergens_list = line.split(" (contains ")
        ingredients = ingredients_list.split()
        allergens = allergens_list.split(", ")
        return Food(set(allergens), set(ingredients))


class Allergen(NamedTuple):
    name: str
    possible_ingredients: Set[str]


def read_data(stream: Iterable[str]) -> List[Food]:
    return [Food.parse(line.strip()) for line in stream]


def get_allergens_ingredients(foods: List[Food]) -> Dict[str, Set[str]]:
    allergens_ingredients: Dict[str, Set[str]] = {}
    for food in foods:
        for allergen in food.allergens:
            ingredients = allergens_ingredients.get(allergen, food.ingredients)
            allergens_ingredients[allergen] = set.intersection(ingredients, food.ingredients)
    return allergens_ingredients


def calc1(foods: List[Food]) -> int:
    allergens_ingredients = get_allergens_ingredients(foods)
    all_ingredients = set.union(*[food.ingredients for food in foods])
    all_possible_allergens = set.union(*list(allergens_ingredients.values()))
    safe_ingredients = all_ingredients - all_possible_allergens

    count = sum(len(set.intersection(food.ingredients, safe_ingredients)) for food in foods)
    return count


def calc2(foods: List[Food]) -> str:
    allergens_ingredients = get_allergens_ingredients(foods)
    found_allergens: Dict[str, str] = {}

    while allergens_ingredients:
        for allergen, ingredients in allergens_ingredients.items():
            if len(ingredients) == 1:
                found_allergens[allergen] = list(ingredients)[0]

        found_ingredients = set(list(found_allergens.values()))

        allergens_ingredients = {
            allergen: ingredients - found_ingredients
            for allergen, ingredients in allergens_ingredients.items()
            if allergen not in found_allergens
        }

    found_ingredients = ",".join([found_allergens[allergen] for allergen in sorted(found_allergens)])
    return found_ingredients


if __name__ == "__main__":
    initial_data = read_data(sys.stdin)

    res1 = calc1(initial_data)
    print(f"result 1: {res1}")

    res2 = calc2(initial_data)
    print(f"result 2: {res2}")
