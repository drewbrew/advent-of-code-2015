from typing import Iterable, Optional


class Sue:

    children: Optional[int] = None
    cats: Optional[int] = None
    samoyeds: Optional[int] = None
    pomeranians: Optional[int] = None
    akitas: Optional[int] = None
    vizslas: Optional[int] = None
    goldfish: Optional[int] = None
    trees: Optional[int] = None
    cars: Optional[int] = None
    perfumes: Optional[int] = None
    part_two = False

    def __init__(self, puzzle_line: str, part_two: bool = False) -> None:
        self.sue_number = 0
        if puzzle_line.startswith("Sue"):
            sue_info, characteristics = puzzle_line.split(":", 1)
            self.sue_number = int(sue_info.split()[1])
        else:
            characteristics = puzzle_line
        for characteristic in characteristics.split(","):
            key, value = characteristic.split(": ")
            setattr(self, key.strip(), int(value))
        self.part_two = part_two

    def is_match(self, other: "Sue") -> bool:
        characteristics = "children,cats,samoyeds,pomeranians,akitas,vizslas,goldfish,trees,cars,perfumes".split(
            ","
        )
        assert all(getattr(other, char) is not None for char in characteristics)
        for characteristic in characteristics:

            if getattr(self, characteristic) is None:
                continue
            if self.part_two and characteristic in {"trees", "cats"}:
                if getattr(self, characteristic) <= getattr(other, characteristic):
                    return False
            elif self.part_two and characteristic in {"pomeranians", "goldfish"}:
                if getattr(self, characteristic) >= getattr(other, characteristic):
                    return False
            elif getattr(self, characteristic) != getattr(other, characteristic):
                return False
        return True


def part_one(puzzle: Iterable[str], part_two: bool = False) -> int:
    match_sue = Sue(
        """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1""".replace(
            "\n", ","
        )
    )
    sues = [Sue(line, part_two=part_two) for line in puzzle]
    matches = [i for i in sues if i.is_match(match_sue)]
    assert len(matches) == 1, len(matches)
    return matches[0].sue_number


def main():
    with open("day16.txt") as infile:
        puzzle = [line for line in infile]
    print(part_one(puzzle))
    print(part_one(puzzle, part_two=True))


if __name__ == "__main__":
    main()
