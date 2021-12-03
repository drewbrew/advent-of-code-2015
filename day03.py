"""day 3: perfectly spherical houses in a vacuum"""

MOVES = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, 1),
    "v": (0, -1),
}
TEST_INPUTS = {
    ">": 2,
    "^>v<": 4,
    "^v^v^v^v^v": 2,
}


def part_one(puzzle: str) -> int:
    places_visited = set()
    position = (0, 0)
    places_visited.add(position)
    for char in puzzle:
        dx, dy = MOVES[char]
        x, y = position
        position = (x + dx, y + dy)
        places_visited.add(position)
    return len(places_visited)


def part_two(puzzle: str) -> int:
    places_visited = set()
    santa_pos = (0, 0)
    bot_pos = (0, 0)
    places_visited.add(santa_pos)
    for index, char in enumerate(puzzle):
        dx, dy = MOVES[char]
        if index % 2:
            # bot
            x, y = bot_pos
            bot_pos = (x + dx, y + dy)
            places_visited.add(bot_pos)
        else:
            # santa
            x, y = santa_pos
            santa_pos = (x + dx, y + dy)
            places_visited.add(santa_pos)
    return len(places_visited)


def main():
    for puzzle, houses in TEST_INPUTS.items():
        assert part_one(puzzle) == houses, (houses, puzzle)
    with open("day03.txt") as infile:
        puzzle = infile.read().strip()
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
