from queue import Queue
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
        input_, output = [i.strip() for i in line.split(' => ')]
        reactions.append((re.compile(input_), output))
    return reactions, input_molecule


def part_one(puzzle: list[str]) -> int:
    reactions, input_molecule = parse_input(puzzle)
    outputs = set()
    for regex, replacement in reactions:
        offsets = [match.start() for match in regex.finditer(input_molecule)]
        for offset in offsets:
            outputs.add(input_molecule[:offset] + regex.sub(replacement, input_molecule[offset:], count=1))

    return len(outputs)


def part_two(puzzle: list[str]) -> int:
    reactions, target = parse_input(puzzle)
    queue = Queue()
    queue.put(('e', 0))
    fewest_steps_found = 1e6
    intermediates_found = {}
    while not queue.empty():
        molecule, steps = queue.get(block=False)
        if steps > fewest_steps_found:
            continue
        try:
            old_score = intermediates_found[molecule]
        except KeyError:
            pass
        else:
            if old_score > steps:
                intermediates_found[molecule] = steps
            else:
                continue
        intermediates_found[molecule] = steps
        for regex, replacement in reactions:
            offsets = [match.start() for match in regex.finditer(molecule)]
            for offset in offsets:
                intermediate = molecule[:offset] + regex.sub(replacement, molecule[offset:], count=1)
                if intermediate == target:
                    print('winner found after', steps)
                    if steps < fewest_steps_found:
                        print('winner found after', steps)
                        fewest_steps_found = steps
                    continue
                if intermediate == molecule or len(intermediate) > len(target):
                    # we're very much on the wrong path as the string can never get shorter
                    continue
                queue.put((intermediate, steps + 1))
    return fewest_steps_found


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 4, part_one_result
    part_two_result = part_two(PART_TWO_TEST)
    with open('day19.txt') as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == '__main__':
    main()