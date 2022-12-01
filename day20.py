"""Day 20: factoring cleverly disguised as elf deliveries"""
from collections import defaultdict

PUZZLE = 33100000


def part_one(puzzle: int) -> int:
    """Find the lowest number where the sum of all factors = puzzle / 10"""
    houses = defaultdict(int)
    for house in range(1, puzzle // 10 + 1):
        for house_number in range(house, puzzle // 10 + 1, house):
            houses[house_number] += house * 10
    print(len(houses))
    return min(house_number for house_number, value in houses.items() if value >= puzzle)


def part_two(puzzle: int) -> int:
    # need to cap at 50 houses
    """Find the lowest number where the sum of all factors = puzzle / 10"""
    houses = defaultdict(int)
    for house in range(1, puzzle // 10 + 1):
        for house_number in range(house, min([puzzle // 10 + 1, house * 50]), house):
            houses[house_number] += house * 11
    print(len(houses))
    return min(house_number for house_number, value in houses.items() if value >= puzzle)


print(part_one(PUZZLE))
print(part_two(PUZZLE))