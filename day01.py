TEST_INPUTS = {
    "(())": 0,
    "()()": 0,
    "(((": 3,
    "(()(()(": 3,
    "())": -1,
    "))(": -1,
    ")))": -3,
    ")())())": -3,
}


def part_one(puzzle_input: str) -> str:
    floor = 0
    for char in puzzle_input:
        floor += 1 if char == "(" else -1
    return floor


def part_two(puzzle_input: str) -> str:
    floor = 0
    for index, char in enumerate(puzzle_input):
        floor += 1 if char == "(" else -1
        if floor == -1:
            return index + 1
    raise ValueError("Oh no!")


def main():
    for puzzle, result in TEST_INPUTS.items():
        assert part_one(puzzle) == result, (puzzle, part_one(puzzle), result)
    with open("day01.txt") as infile:
        puzzle = infile.read().strip()
    print(part_one(puzzle))
    print(part_two(puzzle_input=puzzle))


if __name__ == "__main__":
    main()
