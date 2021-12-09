from itertools import combinations
from collections import Counter

TEST_INPUT = [20, 15, 10, 5, 5]


def part_one(puzzle: list[int], capacity: int = 150) -> int:
    combos = sum(
        (list(combinations(puzzle, length)) for length in range(1, len(puzzle) + 1)),
        start=[],
    )
    return len(list(i for i in combos if sum(i) == capacity))


def part_two(puzzle: list[int], capacity: int = 150) -> int:
    combos = sum(
        (list(combinations(puzzle, length)) for length in range(1, len(puzzle) + 1)),
        start=[],
    )
    candidates = [len(i) for i in combos if sum(i) == capacity]
    count = Counter(candidates)
    return count[min(count)]


def main():
    part_one_result = part_one(TEST_INPUT, 25)
    assert part_one_result == 4, part_one_result
    part_two_result = part_two(TEST_INPUT, 25)
    assert part_two_result == 3, part_two_result
    with open("day17.txt") as infile:
        puzzle = [int(line.strip()) for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
