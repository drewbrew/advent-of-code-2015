from typing import Iterable


def slack(length: int, width: int, height: int) -> int:
    return min([length * width, length * height, width * height,])


def surface_area(length: int, width: int, height: int) -> int:
    return 2 * (length * width + width * height + length * height)


def paper_order(length: int, width: int, height: int) -> int:
    return surface_area(length, width, height) + slack(length, width, height)


def ribbon(length: int, width: int, height: int) -> int:
    perimeter = min(
        [2 * length + width * 2, 2 * width + height * 2, 2 * length + height * 2,]
    )
    return perimeter + length * width * height


def part_one(puzzle_input: Iterable[str]) -> int:
    total = 0
    for line in puzzle_input:
        length, width, height = [int(i) for i in line.split("x")]
        total += paper_order(length, width, height)
    return total


def part_two(puzzle_input: Iterable[str]) -> int:
    total = 0
    for line in puzzle_input:
        length, width, height = [int(i) for i in line.split("x")]
        total += ribbon(length, width, height)
    return total


def main():
    assert slack(2, 3, 4) == 6, slack(2, 3, 4)
    assert surface_area(2, 3, 4) == 52, surface_area(2, 3, 4)
    assert part_one(["2x3x4"]) == 58, part_one(["2x3x4"])
    assert part_one(["1x1x10"]) == 43
    assert ribbon(2, 3, 4) == 34, ribbon(2, 3, 4)
    assert ribbon(1, 1, 10) == 14
    with open("day02.txt") as infile:
        puzzle = [line.strip() for line in infile]

    print(part_one(puzzle_input=puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
