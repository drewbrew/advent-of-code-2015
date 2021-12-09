"""day 15: science for hungry people"""
from dataclasses import dataclass
from typing import Iterable
from itertools import permutations

TEST_INPUT = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3""".splitlines()

PUZZLE = """Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5
Candy: capacity 0, durability 5, flavor -1, texture 0, calories 8
Butterscotch: capacity -1, durability 0, flavor 5, texture 0, calories 6
Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1""".splitlines()


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_input(puzzle: Iterable[str]) -> list[Ingredient]:
    ingredients = []
    for line in puzzle:
        ingredient, params = line.split(": ")
        ingredients.append(
            Ingredient(
                name=ingredient,
                **{
                    entry.split()[0]: int(entry.split()[1])
                    for entry in params.split(", ")
                }
            )
        )
    return ingredients


def part_one(puzzle: Iterable[str], max_amount: int = 100, part_two: bool = False) -> int:
    ingredients = parse_input(puzzle)
    max_score = 0
    perms = list(permutations(ingredients))
    for ingredient_a, ingredient_b, ingredient_c, ingredient_d in perms:
        for a_amount in range(max_amount):
            for b_amount in range(max_amount - a_amount):
                for c_amount in range(max_amount - a_amount - b_amount):
                    d_amount = max_amount - a_amount - b_amount - c_amount
                    capacity_score = max(
                        a_amount * ingredient_a.capacity
                        + b_amount * ingredient_b.capacity
                        + c_amount * ingredient_c.capacity
                        + d_amount * ingredient_d.capacity,
                        0,
                    )
                    durability_score = max(
                        b_amount * ingredient_b.durability
                        + a_amount * ingredient_a.durability
                        + c_amount * ingredient_c.durability
                        + d_amount * ingredient_d.durability,
                        0,
                    )
                    flavor_score = max(
                        a_amount * ingredient_a.flavor
                        + b_amount * ingredient_b.flavor
                        + c_amount * ingredient_c.flavor
                        + d_amount * ingredient_d.flavor,
                        0,
                    )
                    texture_score = max(
                        a_amount * ingredient_a.texture
                        + b_amount * ingredient_b.texture
                        + c_amount * ingredient_c.texture
                        + d_amount * ingredient_d.texture,
                        0,
                    )
                    if part_two:

                        calorie_score = max(
                            a_amount * ingredient_a.calories + b_amount * ingredient_b.calories + c_amount * ingredient_c.calories + d_amount * ingredient_d.calories, 0,
                        )
                        if calorie_score != 500:
                            continue

                    score = (
                        capacity_score * durability_score * flavor_score * texture_score
                    )
                    if score >= max_score:
                        max_score = score
    return max_score


def main():
    print(part_one(PUZZLE))
    print(part_one(PUZZLE, part_two=True))


if __name__ == "__main__":
    main()
