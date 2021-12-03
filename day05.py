import re
from typing import Iterable

VOWEL_REGEX = re.compile(r"[aeiou].*[aeiou].*[aeiou]")
REPEAT_REGEX = re.compile(r"([a-z])\1")
BAD_STRING_REGEX = re.compile(r"(ab|cd|pq|xy)")

P2_REPEAT_REGEX = re.compile(r"([a-z])([a-z]).*\1\2")
P2_AXA_REGEX = re.compile(r"([a-z]).\1")


def is_nice_string(line: str) -> bool:
    if BAD_STRING_REGEX.search(line):
        return False
    if not VOWEL_REGEX.findall(line):
        return False
    if not REPEAT_REGEX.search(line):
        return False
    return True


def is_p2_nice_string(line: str) -> bool:
    return bool(P2_AXA_REGEX.search(line) and P2_REPEAT_REGEX.search(line))


def part_one(puzzle: Iterable[str]) -> int:
    return sum(is_nice_string(line) for line in puzzle)


def part_two(puzzle: Iterable[str]) -> int:
    return sum(is_p2_nice_string(line) for line in puzzle)


def main():
    assert is_nice_string("ugknbfddgicrmopn")
    assert is_nice_string("aaa")
    assert not is_nice_string("jchzalrnumimnmhp")
    assert not is_nice_string("haegwjzuvuyypxyu")
    assert not is_nice_string("dvszwmarrgswjxmb")
    assert is_p2_nice_string("qjhvhtzxzqqjkmpb")
    assert is_p2_nice_string("xxyxx")
    assert not is_p2_nice_string("uurcxstgmygtbstg")
    assert not is_p2_nice_string("ieodomkazucvgmuy")
    with open("day05.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
