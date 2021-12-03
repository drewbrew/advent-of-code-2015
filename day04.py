from hashlib import md5
from itertools import count

TEST_INPUTS = {
    "abcdef": 609043,
    "pqrstuv": 1048970,
}

PUZZLE_INPUT = "iwrupvqb"


def part_one(puzzle: str, num_zeroes: int = 5) -> int:
    counter = count()
    # discard zero to be safe
    next(counter)
    key = ""
    hasher = md5()
    hasher.update(puzzle.encode())
    while not key.startswith("0" * num_zeroes):
        new_hash = hasher.copy()
        new_hash.update(str(next(counter)).encode())
        key = new_hash.hexdigest()
    return next(counter) - 1


def main():
    for puzzle, result in TEST_INPUTS.items():
        assert part_one(puzzle) == result
    print(part_one(PUZZLE_INPUT))
    print(part_one(PUZZLE_INPUT, num_zeroes=6))


if __name__ == "__main__":
    main()
