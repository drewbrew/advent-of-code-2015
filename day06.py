from typing import Iterable


def toggle(
    grid: dict[tuple[int, int], bool],
    start: tuple[int, int],
    end: tuple[int, int],
    part_two: bool = False,
):
    x1, y1 = start
    x2, y2 = end
    x_range = range(x1, x2 + 1) if x2 > x1 else range(x2, x1 + 1)
    y_range = range(y1, y2 + 1) if y2 > y1 else range(y2, y1 + 1)
    for x in x_range:
        for y in y_range:
            if part_two:
                grid[x, y] += 2
            else:
                grid[x, y] = not grid[x, y]


def change_state(
    grid: dict[tuple[int, int], bool],
    start: tuple[int, int],
    end: tuple[int, int],
    state: int | bool,
):
    x1, y1 = start
    x2, y2 = end
    x_range = range(x1, x2 + 1) if x2 > x1 else range(x2, x1 + 1)
    y_range = range(y1, y2 + 1) if y2 > y1 else range(y2, y1 + 1)
    for x in x_range:
        for y in y_range:
            if isinstance(state, bool):
                grid[x, y] = state
            else:
                grid[x, y] += state
                if grid[x, y] < 0:
                    grid[x, y] = 0


def turn_on(
    grid: dict[tuple[int, int], bool], start: tuple[int, int], end: tuple[int, int],
):
    return change_state(grid, start, end, True)


def turn_off(
    grid: dict[tuple[int, int], bool], start: tuple[int, int], end: tuple[int, int],
):
    return change_state(grid, start, end, False)


def increment_brightness(
    grid: dict[tuple[int, int], bool], start: tuple[int, int], end: tuple[int, int],
):
    return change_state(grid, start, end, 1)


def decrement_brightness(
    grid: dict[tuple[int, int], bool], start: tuple[int, int], end: tuple[int, int],
):
    return change_state(grid, start, end, -1)


def part_one(puzzle_input: Iterable[str]) -> int:
    grid = {(x, y): False for x in range(1000) for y in range(1000)}
    for line in puzzle_input:
        words = line.split()
        if words[0] == "toggle":
            start = [int(i) for i in words[1].split(",")]
            end = [int(i) for i in words[3].split(",")]
            toggle(grid, start, end)
        elif words[0] != "turn":
            raise ValueError(f"unknown instruction {line}")
        else:
            func = turn_on if words[1] == "on" else turn_off
            start = [int(i) for i in words[2].split(",")]
            end = [int(i) for i in words[4].split(",")]
            func(grid, start, end)
    return sum(grid.values())


def part_two(puzzle_input: Iterable[str]) -> int:
    grid = {(x, y): False for x in range(1000) for y in range(1000)}
    for line in puzzle_input:
        words = line.split()
        if words[0] == "toggle":
            start = [int(i) for i in words[1].split(",")]
            end = [int(i) for i in words[3].split(",")]
            toggle(grid, start, end, True)
        elif words[0] != "turn":
            raise ValueError(f"unknown instruction {line}")
        else:
            func = increment_brightness if words[1] == "on" else decrement_brightness
            start = [int(i) for i in words[2].split(",")]
            end = [int(i) for i in words[4].split(",")]
            func(grid, start, end)
    return sum(grid.values())


if __name__ == "__main__":
    assert part_one(["turn on 0,0 through 999,999"]) == 1000 * 1000
    assert part_one(["toggle 0,0 through 999,0"]) == 1000
    with open("day06.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))
