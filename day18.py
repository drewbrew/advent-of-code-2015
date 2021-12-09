from typing import Iterable


TEST_INPUT = """.#.#.#
...##.
#....#
..#...
#.#..#
####..""".splitlines()


def parse_input(puzzle: Iterable[str]) -> dict[tuple[int, int], bool]:
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            grid[(x, y)] = char == "#"
    return grid


def is_active(x: int, y: int, grid: dict[tuple[int, int], bool]) -> bool:
    existing_state = grid[x, y]
    if existing_state:
        return sum(
            grid.get((x + dx, y + dy), False)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx, dy) != (0, 0)
        ) in {2, 3}
    return (
        sum(
            grid.get((x + dx, y + dy), False)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx, dy) != (0, 0)
        )
        == 3
    )


def part_one(
    puzzle: Iterable[str], iterations: int = 100, part_two: bool = False
) -> int:
    grid = parse_input(puzzle)
    max_x, max_y = max(grid)
    if part_two:
        grid[0, 0] = True
        grid[max_x, 0] = True
        grid[0, max_y] = True
        grid[max_x, max_y] = True
    for _ in range(iterations):
        grid = {(x, y): is_active(x, y, grid) for (x, y) in grid}
        if part_two:
            grid[0, 0] = True
            grid[max_x, 0] = True
            grid[0, max_y] = True
            grid[max_x, max_y] = True
    return sum(grid.values())


def main():
    part_one_result = part_one(TEST_INPUT, 4)
    assert part_one_result == 4, part_one_result
    part_two_result = part_one(TEST_INPUT, 5, True)
    assert part_two_result == 17, part_two_result
    with open("day18.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_one(puzzle, part_two=True))


if __name__ == "__main__":
    main()
