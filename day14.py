from typing import Iterable


TEST_INPUT = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.""".splitlines()

TEST_TIME = 1000
REAL_TIME = 2503


class Reindeer:
    def __init__(self, speed: int, flying_duration: int, rest_duration: int) -> None:
        self.timer = flying_duration
        self.flying = True
        self.speed = speed
        self.flying_duration = flying_duration
        self.rest_duration = rest_duration
        self.distance_traveled = 0

    def advance_time(self):
        if self.flying:
            self.distance_traveled += self.speed
        self.timer -= 1
        if not self.timer:
            if self.flying:
                self.flying = False
                self.timer = self.rest_duration
            else:
                self.flying = True
                self.timer = self.flying_duration


def part_one(puzzle: Iterable[str], time: int) -> int:
    deer: list[Reindeer] = []
    for line in puzzle:
        words = line.split()
        speed = int(words[3])
        flying_duration = int(words[6])
        rest_duration = int(words[-2])
        deer.append(Reindeer(speed, flying_duration, rest_duration))
    for _ in range(time + 1):
        for character in deer:
            character.advance_time()
    distances = sorted(character.distance_traveled for character in deer)
    return distances[-1]


def part_two(puzzle: Iterable[str], time: int) -> int:
    deer: list[Reindeer] = []
    for line in puzzle:
        words = line.split()
        speed = int(words[3])
        flying_duration = int(words[6])
        rest_duration = int(words[-2])
        deer.append(Reindeer(speed, flying_duration, rest_duration))
    points = [0] * len(deer)
    for _ in range(time + 1):
        for character in deer:
            character.advance_time()
        max_dist = max(i.distance_traveled for i in deer)
        for index, d in enumerate(deer):
            if d.distance_traveled == max_dist:
                points[index] += 1

    return max(points)


def main():
    part_one_result = part_one(TEST_INPUT, TEST_TIME)
    assert part_one_result == 1120, part_one_result
    with open("day14.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle, REAL_TIME))
    print(part_two(puzzle, REAL_TIME))


if __name__ == "__main__":
    main()
