import string
import re

TEST_INPUT = """H => HO
H => OH
O => HH

HOH""".splitlines()

PART_TWO_TEST = """e => H
e => O
H => HO
H => OH
O => HH

HOHOHO""".splitlines()


def parse_input(puzzle: list[str]) -> tuple[tuple[re.Pattern, str], str]:
    assert not puzzle[-2]
    input_molecule = puzzle[-1].strip()
    reactions: list[tuple[re.Pattern, str]] = []
    for line in puzzle[:-2]:
        input_, output = [i.strip() for i in line.split(" => ")]
        reactions.append((re.compile(input_), output))
    return reactions, input_molecule


def part_one(puzzle: list[str]) -> int:
    reactions, input_molecule = parse_input(puzzle)
    outputs = set()
    for regex, replacement in reactions:
        offsets = [match.start() for match in regex.finditer(input_molecule)]
        for offset in offsets:
            outputs.add(
                input_molecule[:offset]
                + regex.sub(replacement, input_molecule[offset:], count=1)
            )

    return len(outputs)


def part_two(puzzle: list[str]) -> int:
    # full credit to
    # https://www.reddit.com/r/adventofcode/comments/3xflz8/comment/cy4etju/
    molecule = puzzle[-1]
    radons = len(list(re.findall("Rn", molecule)))
    argons = len(list(re.findall("Ar", molecule)))
    ys = len(list(re.findall("Y", molecule)))
    total_tokens = len([i for i in molecule if i in string.ascii_uppercase])
    return total_tokens - radons - argons - (2 * ys) - 1


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 4, part_one_result
    with open("day19.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
