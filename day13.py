from itertools import permutations
from collections import defaultdict
from typing import Iterable


TEST_INPUT = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.""".splitlines()


def parse_input(puzzle: Iterable[str]) -> dict[tuple[str, str], int]:
    links = defaultdict(int)
    for line in puzzle:
        words = line.strip().split()
        sign = 1 if words[2] == "gain" else -1
        person_a = words[0]
        person_b = words[-1][:-1]
        units = int(words[3])
        pair = tuple(sorted([person_a, person_b]))
        links[pair] += sign * units
    return links


def part_one(puzzle: Iterable[str], part_two: bool = False) -> int:
    links = parse_input(puzzle)
    people = set(
        sum(list([person_a, person_b] for person_a, person_b in links), start=[],)
    )
    you = "zzz"
    if part_two:
        for other in people:
            links[other, you] = 0
        people.add(you)

    pairings = list(permutations(people))
    score = 0
    for order in pairings:
        running = 0
        for a, b in zip(order[:-1], order[1:]):
            running += links[tuple(sorted([a, b]))]
        running += links[tuple(sorted([order[0], order[-1]]))]
        if running > score:
            score = running
    return score


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 330, part_one_result
    with open("day13.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_one(puzzle, True))


if __name__ == "__main__":
    main()
