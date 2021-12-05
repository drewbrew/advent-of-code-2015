from typing import Iterable
from itertools import permutations

TEST_INPUT = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141""".splitlines()


def parse_input(puzzle: Iterable[str]) -> dict[tuple[str, str], int]:
    graph = {}
    for line in puzzle:
        words = line.split()
        dist = int(words[-1])
        start = words[0]
        dest = words[2]
        graph[start, dest] = graph[dest, start] = dist
    return graph


def part_one(puzzle: Iterable[str]) -> int:
    graph = parse_input(puzzle)
    paths = permutations({x for y in graph for x in y})
    return min(sum(graph[v, w] for v, w in zip(path, path[1:])) for path in paths)


def part_two(puzzle: Iterable[str]) -> int:
    graph = parse_input(puzzle)
    paths = permutations({x for y in graph for x in y})
    return max(sum(graph[v, w] for v, w in zip(path, path[1:])) for path in paths)


def main():
    assert part_one(TEST_INPUT) == 605, part_one(TEST_INPUT)
    puzzle = """AlphaCentauri to Snowdin = 66
AlphaCentauri to Tambi = 28
AlphaCentauri to Faerun = 60
AlphaCentauri to Norrath = 34
AlphaCentauri to Straylight = 34
AlphaCentauri to Tristram = 3
AlphaCentauri to Arbre = 108
Snowdin to Tambi = 22
Snowdin to Faerun = 12
Snowdin to Norrath = 91
Snowdin to Straylight = 121
Snowdin to Tristram = 111
Snowdin to Arbre = 71
Tambi to Faerun = 39
Tambi to Norrath = 113
Tambi to Straylight = 130
Tambi to Tristram = 35
Tambi to Arbre = 40
Faerun to Norrath = 63
Faerun to Straylight = 21
Faerun to Tristram = 57
Faerun to Arbre = 83
Norrath to Straylight = 9
Norrath to Tristram = 50
Norrath to Arbre = 60
Straylight to Tristram = 27
Straylight to Arbre = 81
Tristram to Arbre = 90""".splitlines()
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
