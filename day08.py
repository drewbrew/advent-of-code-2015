from queue import Queue
from typing import Iterable

TEST_INPUTS = {
    '""': (2, 0, 6),
    '"abc"': (5, 3, 9),
    '"aaa\\"aaa"': (10, 7, 16),
    '"\\x27"': (6, 1, 11),
}


def unescaped_str_len(string: str) -> int:
    queue = Queue()
    for char in string:
        queue.put(char)
    length = 0
    while not queue.empty():
        next_char = queue.get(block=False)
        if next_char == "\\":
            char_after = queue.get(block=False)
            if char_after in {'"', "\\"}:
                length += 1
                continue
            if char_after == "x":
                # discard the next two chars
                queue.get(block=False)
                queue.get(block=False)
                length += 1
                continue
            raise ValueError("Unknown char after backslash: " + next_char)
        length += 1
    return length - 2  # every string starts and ends with a quote


def encode(puzzle_line: str) -> str:
    encoded = '"'
    for char in puzzle_line:
        if char == '"':
            encoded += '\\"'
        elif char == "\\":
            encoded += "\\\\"
        else:
            encoded += char
    encoded += '"'
    return encoded


def part_one(puzzle: Iterable[str]) -> int:
    total_lengths = sum(len(line) for line in puzzle)
    unescaped_lengths = sum(unescaped_str_len(line) for line in puzzle)
    return total_lengths - unescaped_lengths


def part_two(puzzle: Iterable[str]) -> int:
    escaped_lengths = sum(len(encode(line)) for line in puzzle)
    total_lengths = sum(len(line) for line in puzzle)
    return escaped_lengths - total_lengths


def main():
    for input_str, (escaped_length, unescaped, encoded_length) in TEST_INPUTS.items():
        assert unescaped_str_len(input_str) == unescaped, (
            unescaped_str_len(input_str),
            unescaped,
            input_str,
        )
        assert len(input_str) == escaped_length
        assert len(encode(input_str)) == encoded_length, len(encode(input_str))
    with open("day08.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
